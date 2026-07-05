from sqlalchemy.orm import Session

from app.models.job_components_log import JobComponentLog


class JobComponentLogDao:

    @staticmethod
    def get_component(
        db: Session,
        job_id,
        layer_type
    ):

        return (
            db.query(JobComponentLog)
            .filter(
                JobComponentLog.job_id == job_id,
                JobComponentLog.layer_type == layer_type
            )
            .first()
        )

    @staticmethod
    def create_component(
        db: Session,
        component: JobComponentLog
    ):

        db.add(component)

        db.commit()

        db.refresh(component)

        return component