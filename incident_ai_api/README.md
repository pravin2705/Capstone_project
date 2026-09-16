# Incident AI API – Week 1 & Week 2
 
## 1. Project Overview
 
This project is an Industrial Incident AI system that helps operators and maintenance teams analyze machine incidents and retrieve relevant maintenance knowledge.
 
The project is divided into two stages:
 
### Week 1 – Incident Intake & GenAI Foundation
 
Week 1 focuses on:
 
- Receiving incident information through a FastAPI API
- Validating input data
- Classifying incident type
- Determining incident severity
- Extracting structured facts
- Generating a diagnostic summary
- Creating an AI provider abstraction
- Handling exceptions
- Testing the API and business logic
 
### Week 2 – Maintenance Knowledge RAG
 
Week 2 adds a Retrieval-Augmented Generation (RAG) capability.
 
The RAG system:
 
- Reads maintenance manuals and SOP documents
- Splits documents into smaller chunks
- Creates searchable representations of chunks
- Stores document metadata
- Filters documents using machine model and manual version
- Retrieves relevant maintenance evidence
- Uses semantic and keyword-based retrieval
- Evaluates retrieval quality
- Improves poor retrieval results
- Returns evidence with source information
 
---
 
# 2. Business Problem
 
Industrial machines generate alarms such as:
 
- High temperature
- Excessive vibration
- High pressure
- Oil leakage
 
The system should help answer:
 
> "What should the maintenance engineer check for this alarm?"
 
The answer should come from the correct maintenance document and correct machine model/version.
 
For example:
 
```text
Asset       : PUMP-101
Model       : PX-500
Version     : 3.2
Alarm       : High temperature
 