import re

class EmailClassifier:
    def __init__(self):
        self.rejection_keywords = [
            'regret', 'unfortunately', 'not selected', 'not moving forward',
            'decided to pursue', 'other candidates', 'not a fit', 'decline',
            'unable to offer', 'not proceed', 'thank you for your interest',
            'better match', 'competitive', 'keep your resume on file',
            'different direction', 'position has been filled'
        ]
        
        self.selection_keywords = [
            'congratulations', 'pleased to', 'happy to inform', 'selected',
            'shortlisted', 'next round', 'interview', 'offer', 'move forward',
            'excited to', 'impressed', 'would like to schedule', 'extend an offer',
            'finalist', 'successful', 'advancing', 'invitation'
        ]
        
        self.pending_keywords = [
            'under review', 'reviewing', 'received your application',
            'application submitted', 'will be in touch', 'currently reviewing',
            'being reviewed', 'considering', 'processing', 'evaluating'
        ]
    
    def classify(self, subject, body):
        """Classify email based on subject and body content"""
        text = f"{subject} {body}".lower()
        
        # Count keyword matches
        rejection_score = sum(1 for kw in self.rejection_keywords if kw in text)
        selection_score = sum(1 for kw in self.selection_keywords if kw in text)
        pending_score = sum(1 for kw in self.pending_keywords if kw in text)
        
        # Determine classification
        scores = {
            'Rejection': rejection_score,
            'Selection': selection_score,
            'Pending': pending_score
        }
        
        max_score = max(scores.values())
        
        if max_score == 0:
            return 'Pending'  # Default to pending if no keywords match
        
        # Return category with highest score
        return max(scores, key=scores.get)
