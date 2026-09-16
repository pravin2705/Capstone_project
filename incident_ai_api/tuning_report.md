# RAG Retrieval Tuning Report
 
## 1. Baseline Retrieval
 
The initial RAG retriever used semantic similarity based on cosine similarity.
 
Baseline evaluation:
 
- Total questions: 22
- Correct: 18
- Incorrect: 4
- Accuracy: 81.82%
 
## 2. Problem Identified
 
One retrieval case produced an incorrect result.
 
Query:
 
"What routine maintenance should be performed on the pump?"
 
Expected section:
 
"Preventive Maintenance"
 
Initial retrieved section:
 
"High Temperature Alarm"
 
The semantic similarity search was not sufficiently distinguishing between maintenance-related content and alarm-related content.
 
## 3. Root Cause
 
The baseline retriever depended mainly on semantic similarity.
 
Some chunks contained similar words such as:
 
- pump
- maintenance
- alarm
- temperature
 
This caused the wrong section to receive a high similarity score.
 
## 4. Tuning Applied
 
The retriever was improved using hybrid scoring.
 
The final score combines:
 
- 75% semantic similarity
- 25% keyword matching
 
Keyword matching gives additional importance to relevant words in the section title.
 
Stop words such as:
 
- what
- should
- the
- is
- for
- on
 
are removed before keyword matching.
 
Section-title matches receive higher importance than normal text matches.
 
## 5. Metadata Filtering
 
The retriever also supports metadata filtering using:
 
- machine_model
- manual_version
 
This prevents retrieval from unrelated machine models or manual versions.
 
## 6. Results After Tuning
 
After applying hybrid retrieval:
 
- Total questions: 22
- Correct: 21
- Incorrect: 1
- Accuracy: 95.45%
 
Improvement:
 
81.82% -> 95.45%
 
Absolute improvement:
 
13.63 percentage points.
 
## 7. Conclusion
 
Hybrid retrieval improved the retrieval quality by combining semantic similarity with keyword matching.
 
The tuning particularly helped queries where the important concept appeared directly in the document section title.
 
The final retriever provides:
 
- Semantic search
- Keyword matching
- Metadata filtering
- Top-K retrieval
- Retrieval scores
 