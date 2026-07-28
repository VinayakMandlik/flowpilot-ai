from app.services.intent_router import Intent
from app.pipelines.rag_pipeline import RagPipeline
from app.pipelines.general_pipeline import GeneralPipeline
from app.pipelines.hybrid_pipeline import HybridPipeline


class PipelineFactory:

    _pipelines = {
        Intent.RAG: RagPipeline,
        Intent.GENERAL: GeneralPipeline,
        Intent.HYBRID: HybridPipeline,
    }

    @classmethod
    def get(cls, intent: Intent):

        pipeline = cls._pipelines.get(intent)

        if pipeline is None:
            raise NotImplementedError(
                f"{intent.value} pipeline is not implemented."
            )

        return pipeline