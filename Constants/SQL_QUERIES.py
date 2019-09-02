# Emotions based on subreddit
SELECT_GROUPED_EMOTIONS = """
select a.subred,sum(s.anger) ang, sum(s.anticipation) anti, sum(s.disgust) dis, sum(s.fear) fear, sum(s.joy) joy, sum(s.sadness) sad, sum(s.surprise) surp, sum(s.trust) trus 
from comment_sentiment as s
join comment_atr as a on
a.com_id = s.com_id
where a.subred = %s
group by 1
"""