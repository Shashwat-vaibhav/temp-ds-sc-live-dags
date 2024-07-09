from enum import Enum


# Please do not add new pods to this class, without approval from repository owners.
# This is important for attribution purposes
class Pod(Enum):
    SC_FEED_RANKING = "sc-feed-ranking"
    SC_FEED_CONTENT_JOURNEY = "sc-feed-content-journey"
    SC_FEED_DELIVERY = "sc-feed-delivery"
    SC_FEED_NOTIFICATIONS = "sc-feed-notifications"
    SC_AI_CONTENT_MODERATION = "sc-ai-content-moderation"
    SC_AI_CONTENT_UNDERSTANDING = "sc-ai-content-understanding"
    SC_FEED_LIVE = "sc-feed-live"
    SC_FEED_BALANCER = "sc-feed-balancer"
    SC_FEED_FEATURES = "sc-feed-features"
    SC_AI_UNASSIGNED = "sc-ai-unassigned"
    EXP_SCIENCES = "e13n-sciences"
    SUPPLY_AI = "supply-ai-team"
