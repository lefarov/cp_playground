I'm preparing for an ML system design interview in Meta for IC6 level (staff ML engineer) and want to do a mock interveiw.
Plese think of a question and act as my interviewer.
We'll work through it step by step.
I'll ask follow-up questions, but please don't give me all informations and hints at once.
Here're some notest from the recruiter on how I should structure my response and how it will be evaluated.
This should help you to build a scenario.

- Problem navigation
    - reactive system or pre-emptive system
    - react to flagging
    - num of published listings per day
    - latency requirements
    - should just flag whether it’s gun or not and pass it down to another system
        - human review or anything (false positives are not that bad)
        - or do we have authority to take it down (false positives can be detrimental to use experience)
    - do we have any constraints on how fast it should be detected (legal or otherwise)
    - any hard constraints on false-positives/negatives (maybe legal?)
        - business constraints
    - any other stakeholders I should be aware of?
    - Options:
        - classification ML system at listing creation path
            - block listing creation path
        - async ML system
            - non-blocking listing creation path
            - async batch processing of new listings
    - baselines
- Data
    - listing → firearm / not a firearm
        - if some system is already in place (like human review) collect past data from it
        - contract human annotators
        - use LLM/VLM to generate synthetic data points
    - listing’s metadata
        - textual description
        - picture (if present)
        - if on async path (comments under the listing)
    - sellers prior activity on the platform (this we should clarify from the business might cuase some bias discussion)
        - num of sales
        - days since registration
        - prior suspected policy violations
        - rating, etc
    - user’s interactions with this data
- Feature engineering
    - textual description + image + comments → VLM to get an embedding
        - bag of words
        - hits for particular words
        - possible fine-tune OSS VLM to produce better embedding for this task (or maybe use it as the model itself depends on which path we’re and what are latency constraints)
    - sellers prior activity
        - num of sales, days since registration → Z-norm
        - rating → OHE
        - prior suspected policy violation → bool or binary encoding
    - user’s interactions with this data
        - num of buys, num of comments → Z-norm
        - can we use colab embeddings somehow?
            - two-tower model for the listing
            - avrg cossim with the users that bought
- Modeling
    - if trigger-based or async, we can just use VLM (we would need to use it to compute embedding in any case) we can as well fine tune that to do predictions
    - if we need make sure that we use sellers prior activity and user interactions data we can use a simple MLP on top of the VLM embeddings with the features we’ve discussed
    - binary cross-entropy loss
    - if we need the uncertainty estimate (ultimately we could go to BNN) but we can start with sampling-based estimates of uncertainty)
    - make sure model is calibrated (i.e. outputs true probability), then threshold can be decided by business
- Metrics:
    - model-specific offline:
        - AUC_PR (if we have imbalanced dataset)
        - calibration curve
    - online:
        - PR or just recall
    - business metrics:
        - time to detect
        - added latency


The probelms that we already worked through previously:
- fire-arms detection on markeplace
- harmful emerging trend detection on video platform i.e. instagram
- detecting coordinated networks of bad actors in professional medid platform, i.e. LinkedIn
- let's try something that's not relient on outlier detection

Feel free to ask questions outside Meta product offerings.

Please, when I ask follow-up questions don't give me obvious hints that would also imply which modeling approach I should use.
Answer shorter.