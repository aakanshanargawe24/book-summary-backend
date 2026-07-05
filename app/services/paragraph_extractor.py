import time
from google import genai
from google.genai.errors import APIError
from app.models.job_components_log import JobComponentLog

# Initialize the modern SDK client
client = genai.Client()


class ParagraphExtractor:

    @staticmethod
    def extract(db, component_log_id, book_id):
        db_session = db

        print(f"\n--- New Extraction Triggered ---")
        print(f"Book ID: {book_id}")
        print(f"Component Log ID: {component_log_id}")

        try:
            # ID se database mein record dhoondhte hain
            log_item = db_session.query(JobComponentLog).filter(
                JobComponentLog.id == component_log_id
            ).first()

            if not log_item:
                print(f"[Database Note] Entry with ID {component_log_id} strictly does not exist in DB.")
                return

            print(
                f"[Database Found] Record Status in DB is currently: '{log_item.status}' | Layer Type: '{getattr(log_item, 'layer_type', 'N/A')}'")

            # Agar status already completed ya failed hai, toh skip karo
            if log_item.status in ['completed', 'failed']:
                print(f"[Skip] Task is already {log_item.status}.")
                return

            # AGAR STATUS 'pending' HAI, TOH USE 'processing' SET KARO
            if log_item.status == 'pending':
                print(f"[Status Update] Changing status from 'pending' to 'processing'...")
                log_item.status = 'processing'
                db_session.commit()

            text_content = log_item.current_paragraph_cursor
            if not text_content:
                print(f"[Warning] Text content (current_paragraph_cursor) is empty for this row!")
                # Agar khali text hai, toh ise completed ya failed mark kar do taaki loop na bane
                log_item.status = "completed"
                db_session.commit()
                return

            prompt = f"Process and clean the following book paragraph:\n\n{text_content}"

            success = False
            attempts = 0
            max_retries = 3

            while not success and attempts < max_retries:
                try:
                    print("Calling Gemini API...")

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    # Update status to completed after Gemini response
                    log_item.status = "completed"
                    db_session.commit()

                    success = True
                    print(f"🎉 Success! Paragraph {component_log_id} processed and completed!")

                    # 429 Protection Delay
                    time.sleep(6)

                except APIError as e:
                    if e.code == 429:
                        attempts += 1
                        print(f"[Gemini 429] Rate limit hit. Waiting 60s...")
                        db_session.rollback()
                        time.sleep(60)
                    else:
                        print(f"[Gemini Error] Code {e.code}: {e.message}")
                        log_item.status = "failed"
                        db_session.commit()
                        raise e

        except Exception as e:
            print(f"[ExtractionManager Error] System Engine Failure: {e}")
            db_session.rollback()
            raise e