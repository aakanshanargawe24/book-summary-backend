from app.core.enums import LayerTypeEnum

from app.dao.job_component_logs_dao import JobComponentLogDao
from app.services.paragraph_extractor import ParagraphExtractor
from app.models.job_components_log import JobComponentLog


class Orchestrator:

    @staticmethod
    def process(
        db,
        job_id,
        book_id
    ):

        component = JobComponentLogDao.get_component(
            db=db,
            job_id=job_id,
            layer_type=LayerTypeEnum.PARAGRAPH
        )

        if component is None:

            component = JobComponentLog(
                job_id=job_id,
                layer_type=LayerTypeEnum.PARAGRAPH
            )

            component = JobComponentLogDao.create_component(
                db=db,
                component=component
            )

        ParagraphExtractor.extract(
            db=db,
            component_log_id=component.id,
            book_id=book_id
        )