# Incident AI API - Architecture
 
## High-Level Architecture
 
```text
                    OPERATOR
                    |
                    v
             Incident Request
                    |
                    v
              FastAPI API
                    |
                    v
             Input Validation
                    |
                    v
          Incident Classification
                    |
                    v
          Incident Type + Severity
                    |
                    v
          Maintenance RAG System
                    |
          +---------+---------+
          |                   |
          v                   v
    Metadata Filter       Retrieval
    Model/Version       Vector/Keyword
          |                   |
          +---------+---------+
                    |
                    v
             Relevant Chunks
                    |
                    v
          Grounded Diagnostic
               Guidance
                    |
                    v
               Citations
                    |
                    v
              Final Response
 