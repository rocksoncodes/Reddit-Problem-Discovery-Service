from orchestrators.ingress_orchestrator import IngressOrchestrator
from orchestrators.sentiment_orchestrator import SentimentOrchestrator
from orchestrators.core_orchestrator import CoreOrchestrator
from orchestrators.egress_orchestrator import EgressOrchestrator
from config import settings

if __name__ == "__main__":
    ingress = IngressOrchestrator()
    sentiment = SentimentOrchestrator()
    core = CoreOrchestrator()
    egress = EgressOrchestrator()
    
    ingress.run()
    sentiment.run()
    core.run()
    egress.run(settings.CHOICE_THREE)
