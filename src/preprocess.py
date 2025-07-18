from langchain_core.documents import Document

def preprocess_for_langchain(ics_data):
    docs = []
    for incident in ics_data:
        summary = incident.get("summary", "No summary.")
        asset = ", ".join(incident.get("asset", {}).get("variety", []))
        threat_actor = ", ".join(incident.get("actor", {}).get("external", {}).get("variety", []))
        timeline = incident.get("timeline", {}).get("incident", "Unknown date")

        content = f"""
        ICS Incident Summary:
        Date: {timeline}
        Asset Type: {asset}
        Threat Actor: {threat_actor}
        Description: {summary}
        """
        docs.append(Document(page_content=content.strip()))
    return docs
