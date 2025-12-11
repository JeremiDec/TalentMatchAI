# GraphRAG vs Naive RAG Comparison Results

## Summary
- **GraphRAG Wins**: 8
- **Naive RAG Wins**: 0
- **Ties**: 34
- **GraphRAG Win Rate**: 19.0%

- **GraphRAG Avg Quality**: 0.04
- **Naive RAG Avg Quality**: 0.00

## Performance by Category

### Counting
- GraphRAG: 0/6 (0.0%)

### Filtering
- GraphRAG: 0/6 (0.0%)

### Aggregation
- GraphRAG: 2/6 (33.3%)

### Sorting
- GraphRAG: 2/6 (33.3%)

### Multi_Hop_Reasoning
- GraphRAG: 3/6 (50.0%)

### Temporal_Reasoning
- GraphRAG: 1/6 (16.7%)

### Complex_Combinations
- GraphRAG: 0/6 (0.0%)

## Detailed Results

| # | Question | Category | GraphRAG Answer | Naive RAG Answer | Ground Truth | Winner |
|---|----------|----------|-----------------|------------------|--------------|--------|
| 1 | How many people have Python programming skills? | counting | There are 139 people with Pyth... | The context provided does not ... | 12 | Tie ⚖️ |
| 2 | How many people have worked at Google? | counting | There are 0 people who have wo... | The context provided does not ... | Zero | Tie ⚖️ |
| 3 | What is the total number of people with AWS certif... | counting | There are 0 people with AWS ce... | The context provided does not ... | 10 | Tie ⚖️ |
| 4 | How many people have Master's degrees? | counting | There are 0 people who have Ma... | The context provided does not ... | Zero | Tie ⚖️ |
| 5 | How many people are located in San Francisco? | counting | There are 0 people located in ... | The context provided does not ... | Zero | Tie ⚖️ |
| 6 | How many people have both Docker and Kubernetes sk... | counting | There are 40 people who have b... | The context provided does not ... | 6 | Tie ⚖️ |
| 7 | List all people who have both React and Node.js sk... | filtering | The following people have both... | The context provided does not ... | Thomas Scott, Andrew Butler, G... | Tie ⚖️ |
| 8 | Find all developers with more than 5 years of Pyth... | filtering | I don't know the answer. | I cannot determine the develop... | None | Tie ⚖️ |
| 9 | Show me people who have AWS certifications and wor... | filtering | I don't know the answer. | The context provided does not ... | Thomas Scott, Andrew Butler, G... | Tie ⚖️ |
| 10 | Find all people who studied Computer Science and h... | filtering | I don't know the answer. | Based on the provided context,... | Sandra Garcia, Thomas Scott, A... | Tie ⚖️ |
| 11 | List people who worked at both startups and large ... | filtering | I don't know the answer. | The context provided does not ... | None | Tie ⚖️ |
| 12 | Find all senior developers with leadership experie... | filtering | I don't know the answer. | The context provided does not ... | Sandra Garcia, Thomas Scott, A... | Tie ⚖️ |
| 13 | What is the average years of experience across all... | aggregation | I don't know the answer to the... | I cannot determine the average... | 5.2 | Tie ⚖️ |
| 14 | What is the most common programming language skill... | aggregation | The most common programming la... | The context provided does not ... | JavaScript | Tie ⚖️ |
| 15 | What is the average number of skills per person? | aggregation | The average number of skills p... | I cannot determine the average... | 8.5 | GraphRAG ✅ |
| 16 | Which city has the most candidates? | aggregation | The city with the most candida... | The context provided does not ... | Port Vincent | Tie ⚖️ |
| 17 | What percentage of people have cloud certification... | aggregation | Error: {code: Neo.ClientError.... | The context provided does not ... | 30 | GraphRAG ✅ |
| 18 | What is the most frequently mentioned company? | aggregation | The most frequently mentioned ... | I cannot determine the most fr... | Tech Innovations Inc. | Tie ⚖️ |
| 19 | Who are the top 3 most experienced developers? | sorting | The top 3 most experienced dev... | I cannot determine the top 3 m... | Jonathan Weeks, Jason Ramirez,... | Tie ⚖️ |
| 20 | List the 5 people with the most programming langua... | sorting | I don't know the answer. | I cannot determine the names o... | Cynthia Zuniga, Devon Kennedy,... | Tie ⚖️ |
| 21 | Rank all candidates by their number of certificati... | sorting | Here are the candidates ranked... | I cannot determine the number ... | 1. Jonathan Weeks
2. Zachary H... | GraphRAG ✅ |
| 22 | Who has the most diverse skill set? | sorting | Anne Kim has the most diverse ... | I cannot determine who has the... | Cynthia Zuniga, Thomas Scott, ... | Tie ⚖️ |
| 23 | List people in order of their career progression | sorting | Based on the information provi... | I'm unable to provide a list o... | Sandra Garcia, Thomas Scott, A... | Tie ⚖️ |
| 24 | Which candidates have the most company experience? | sorting | The candidate with the most co... | I cannot determine which candi... | Jonathan Weeks, Zachary Huff, ... | GraphRAG ✅ |
| 25 | Find all pairs of people who attended the same uni... | multi_hop_reasoning | There are 10 pairs of people w... | I cannot determine any pairs o... | Port Vincent: Sandra Garcia, T... | GraphRAG ✅ |
| 26 | Which people have worked at the same companies? | multi_hop_reasoning | Adam Fowler has worked at Tech... | I cannot determine which peopl... | Sandra Garcia, Thomas Scott, A... | GraphRAG ✅ |
| 27 | Find developers who have complementary skills for ... | multi_hop_reasoning | I don't know the answer. | Based on the provided context,... | Sandra Garcia, Thomas Scott, A... | Tie ⚖️ |
| 28 | Identify people who could mentor others based on s... | multi_hop_reasoning | There are 10 mentors who could... | I cannot determine specific in... | Sandra Garcia, Thomas Scott, A... | Tie ⚖️ |
| 29 | Find all connections between people through shared... | multi_hop_reasoning | There are 10 connections invol... | I cannot determine any connect... | Tech Innovations Inc.: Sandra ... | GraphRAG ✅ |
| 30 | Which people have similar career paths? | multi_hop_reasoning | There are 10 people who have s... | I cannot determine which peopl... | Sandra Garcia, Thomas Scott, A... | Tie ⚖️ |
| 31 | Who graduated most recently? | temporal_reasoning | The most recent graduate is Jo... | I cannot determine who graduat... | Kaitlin Miller | Tie ⚖️ |
| 32 | Find people who started their careers in the same ... | temporal_reasoning | There are 10 records of indivi... | I cannot determine the specifi... | Sandra Garcia, Thomas Scott, A... | Tie ⚖️ |
| 33 | Which certifications were obtained in the last 2 y... | temporal_reasoning | I don't know the answer. | The context provided does not ... | Certified Kubernetes Administr... | Tie ⚖️ |
| 34 | Who has the longest tenure at a single company? | temporal_reasoning | The individual with the longes... | The context provided does not ... | None | Tie ⚖️ |
| 35 | Find people who changed careers after 2020 | temporal_reasoning | I don't know the answer. | The provided context does not ... | None | Tie ⚖️ |
| 36 | Which candidates have the most recent work experie... | temporal_reasoning | The candidates with the most r... | I cannot determine which candi... | Zachary Huff, Devon Kennedy, K... | GraphRAG ✅ |
| 37 | Find Python developers with AWS certifications who... | complex_combinations | I don't know the answer. | Based on the provided context,... | None | Tie ⚖️ |
| 38 | List all senior developers with both frontend and ... | complex_combinations | I don't know the answer. | The context provided does not ... | Sandra Garcia, Thomas Scott, A... | Tie ⚖️ |
| 39 | Find people with machine learning skills who worke... | complex_combinations | The information provided does ... | Based on the provided context,... | Sandra Garcia, Thomas Scott, A... | Tie ⚖️ |
| 40 | Identify candidates with both technical skills and... | complex_combinations | There are 10 candidates who po... | Based on the provided context,... | Sandra Garcia, Thomas Scott, A... | Tie ⚖️ |
| 41 | Find full-stack developers with startup experience... | complex_combinations | I don't know the answer. | Based on the provided context,... | None | Tie ⚖️ |
| 42 | List all candidates suitable for a DevOps role bas... | complex_combinations | I don't know the answer. | I cannot determine the candida... | Sandra Garcia, Thomas Scott, A... | Tie ⚖️ |