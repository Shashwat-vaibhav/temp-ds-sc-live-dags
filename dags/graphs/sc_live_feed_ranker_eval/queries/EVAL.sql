DECLARE fromtime TIMESTAMP DEFAULT TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 5 HOUR);
DECLARE totime TIMESTAMP DEFAULT CURRENT_TIMESTAMP();

create or replace table `maximal-furnace-783.sc_livestream_data.eval_sc_live_feed_multi_obj_ranker` as

with views as (
    select max(a.time) as time, a.distinct_id, a.chatRoomId, a.requestId from `maximal-furnace-783.sc_analytics.chatroom_discoveryPage_view_v2` a
WHERE a.time between fromtime and totime and a.requestId is not null
group by 2,3,4
    ),

    base as (
select max(a.time) as time, a.distinct_id, a.chatRoomId, a.requestId from `maximal-furnace-783.sc_analytics.group_chat_joined` a
where a.time between fromtime and totime and a.requestId is not null
group by 2,3,4
    ),

    view_join as (
select distinct a.distinct_id, a.chatRoomId, a.requestId, if(b.chatRoomId is null, 0, 1) as join_label  from views a
    left join base b
on a.distinct_id=b.distinct_id and a.chatRoomId=b.chatroomId and a.requestId=b.requestId
    ),

    acj as (
select distinct a.distinct_id, a.chatroomId, a.requestId from `maximal-furnace-783.sc_analytics.audio_chat_joined_or_left`  a
where requestId is not null and a.time between fromtime and totime and audioChatStatus=1
    ),

    tcm as (
select distinct a.distinct_id, a.chatroomId, a.requestId from `maximal-furnace-783.sc_analytics.tag_chat_message_sent` a
where requestId is not null and a.time between fromtime and totime and a.messageId is not null
    ),

    gift as (
select distinct a.distinct_id, a.chatroomId, a.requestId from `maximal-furnace-783.sc_analytics.virtual_gifting_gift_sent` a
where requestId is not null and a.time between fromtime and totime
    ),

    cr as (
select *except(name, eventsPlatformSource, eventUuid, ntp_eventRecordTime_ms, ntp_eventDispatchTime_ms, serverTime_ms, eventIngestionTime_ms, packetId, categoryId, chatroomL0Category_LIFETIME, chatroomL1Category_LIFETIME, hostId, coHostId) from `maximal-furnace-783.sc_analytics.sc_live_ranker_chatroom_event`
where time between fromtime and totime and feedType = 'chatFeed' and (requestId is not null and requestId != '' and length(requestId) > 0) and combinedRankerScore IS NOT NULL
    ),

    user as (
select *except(name, eventsPlatformSource, eventUuid, ntp_eventRecordTime_ms, ntp_eventDispatchTime_ms, serverTime_ms, eventIngestionTime_ms, packetId) from `maximal-furnace-783.sc_analytics.sc_live_ranker_user_event`
where time between fromtime and totime and feedType = 'chatFeed' and (requestId is not null and requestId != '' and length(requestId) > 0)
    ),

    cr_features as (
select b.distinctId as userId , a.*, b.*except(distinctId,time,requestId,feedType,sessionId,clientRequestId) from cr a
    inner join user b
on a.requestId=b.requestId
    ),

    ranker_features as (
select a.*, b.join_label,
    if(c.distinct_id is null,0,1) as acj_label,
    if(d.distinct_id is null , 0, 1) as tcm_label,
    if(g.distinct_id is null, 0, 1) as gift_label
from cr_features a
    inner join view_join b
on a.userId=b.distinct_id and a.requestId=b.requestId and a.cId=b.chatroomId
    left join acj c
    on a.userId=c.distinct_id and a.cId=c.chatroomId and a.requestId=c.requestId
    left join tcm d
    on a.userId=d.distinct_id and a.cId=d.chatroomId and a.requestId=d.requestId
    left join gift g
    on a.userId=g.distinct_id and a.cId=g.chatroomId and a.requestId=g.requestId
    )

select distinct
    exptId,
    variant,
    combinedRankerScore,
    feedModelAcjScore,
    feedModelGiftScore,
    feedModelJoinScore,
    feedModelTcmScore,
    join_label,
    acj_label,
    tcm_label,
    gift_label,
    chatroomJoinCount_15_MINUTE,
    chatroomJoinCount_1_HOUR,
    chatroomJoinCount_6_HOUR,
    chatroomJoinCount_1_DAY,
    chatroomJoinCount_3_DAY,
    chatroomJoinCount_7_DAY,
    chatroomGiftAmount_15_MINUTE,
    chatroomGiftAmount_1_DAY,
    chatroomGiftAmount_1_HOUR,
    chatroomGiftAmount_3_DAY,
    chatroomGiftAmount_6_HOUR,
    chatroomGiftAmount_7_DAY,
    chatroomGiftCount_15_MINUTE,
    chatroomGiftCount_1_HOUR,
    chatroomGiftCount_6_HOUR,
    chatroomGiftCount_1_DAY,
    chatroomGiftCount_3_DAY,
    chatroomGiftCount_7_DAY,
    chatroomCommentCount_15_MINUTE,
    chatroomCommentCount_1_HOUR,
    chatroomCommentCount_6_HOUR,
    chatroomCommentCount_1_DAY,
    chatroomCommentCount_3_DAY,
    chatroomCommentCount_7_DAY,
    chatroomBattleCount_15_MINUTE,
    chatroomBattleCount_1_HOUR,
    chatroomBattleCount_6_HOUR,
    chatroomBattleCount_1_DAY,
    chatroomBattleCount_3_DAY,
    chatroomBattleCount_7_DAY,
    distinctChatroomGiftersCount_15_MINUTE,
    distinctChatroomGiftersCount_1_HOUR,
    distinctChatroomGiftersCount_6_HOUR,
    distinctChatroomGiftersCount_1_DAY,
    distinctChatroomGiftersCount_3_DAY,
    distinctChatroomGiftersCount_7_DAY,
    chatroomCurrentActiveCount_LIFETIME,
    chatroomAvailableSeatCount_LIFETIME,
    chatroomMinGiftAmount_LIFETIME,
    chatroomMaxGiftAmount_LIFETIME,
    time_lastGiftTime_LIFETIME,
    time_lastCommentTime_LIFETIME,
    time_lastAudioSeatRequestedTime_LIFETIME,
    time_lastGmvTime_LIFETIME,
    time_lastChatroomJoinedTime_LIFETIME,
    embScore,
    userGiftAmount_1_DAY,
    userGiftAmount_3_DAY,
    userGiftAmount_7_DAY,
    userGiftAmount_1_HOUR,
    userGiftAmount_6_HOUR,
    userGiftAmount_15_MINUTE,
    userCommentCount_1_DAY,
    userCommentCount_3_DAY,
    userCommentCount_7_DAY,
    userCommentCount_1_HOUR,
    userCommentCount_6_HOUR,
    userCommentCount_15_MINUTE,
    userRequestAudioSeatCount_1_DAY,
    userRequestAudioSeatCount_3_DAY,
    userRequestAudioSeatCount_7_DAY,
    userRequestAudioSeatCount_1_HOUR,
    userRequestAudioSeatCount_6_HOUR,
    userRequestAudioSeatCount_15_MINUTE,
    userRechargeCount_1_DAY,
    userRechargeCount_3_DAY,
    userRechargeCount_7_DAY,
    userRechargeCount_1_HOUR,
    userRechargeCount_6_HOUR,
    userRechargeCount_15_MINUTE,
    userHostChatroomCount_1_DAY,
    userHostChatroomCount_3_DAY,
    userHostChatroomCount_7_DAY,
    userHostChatroomCount_1_HOUR,
    userHostChatroomCount_6_HOUR,
    userHostChatroomCount_15_MINUTE,
    userHostGmvAmount_1_DAY,
    userHostGmvAmount_3_DAY,
    userHostGmvAmount_7_DAY,
    userHostGmvAmount_1_HOUR,
    userHostGmvAmount_6_HOUR,
    userHostGmvAmount_15_MINUTE,
    distinctChatroomJoinCount_15_MINUTE,
    distinctChatroomJoinCount_1_HOUR,
    distinctChatroomJoinCount_6_HOUR,
    distinctChatroomJoinCount_1_DAY,
    distinctChatroomJoinCount_3_DAY,
    distinctChatroomJoinCount_7_DAY,
    distinctChatroomCommentersCount_15_MINUTE,
    distinctChatroomCommentersCount_1_HOUR,
    distinctChatroomCommentersCount_6_HOUR,
    distinctChatroomCommentersCount_1_DAY,
    distinctChatroomCommentersCount_3_DAY,
    distinctChatroomCommentersCount_7_DAY,
    userGiftAmount_1_MINUTE,
    userGiftAmount_5_MINUTE,
    userCommentCount_1_MINUTE,
    userCommentCount_5_MINUTE,
    userRequestAudioSeatCount_1_MINUTE,
    userRequestAudioSeatCount_5_MINUTE,
    userRechargeCount_1_MINUTE,
    userRechargeCount_5_MINUTE,
    userHostChatroomCount_1_MINUTE,
    userHostChatroomCount_5_MINUTE,
    userHostGmvAmount_1_MINUTE,
    userHostGmvAmount_5_MINUTE,
    chatroomJoinCount_1_MINUTE,
    chatroomJoinCount_5_MINUTE,
    chatroomGiftAmount_1_MINUTE,
    chatroomGiftAmount_5_MINUTE,
    chatroomGiftCount_1_MINUTE,
    chatroomGiftCount_5_MINUTE,
    chatroomCommentCount_1_MINUTE,
    chatroomCommentCount_5_MINUTE,
    chatroomBattleCount_1_MINUTE,
    chatroomBattleCount_5_MINUTE,
    chatroomRequestAudioSeatCount_1_MINUTE,
    chatroomRequestAudioSeatCount_5_MINUTE,
    chatroomRequestAudioSeatCount_15_MINUTE,
    chatroomRequestAudioSeatCount_1_HOUR,
    chatroomRequestAudioSeatCount_6_HOUR,
    chatroomRequestAudioSeatCount_1_DAY,
    chatroomRequestAudioSeatCount_3_DAY,
    chatroomRequestAudioSeatCount_7_DAY,
    distinctChatroomGiftersCount_1_MINUTE,
    distinctChatroomGiftersCount_5_MINUTE,
    distinctChatroomJoinCount_1_MINUTE,
    distinctChatroomJoinCount_5_MINUTE,
    distinctChatroomCommentersCount_1_MINUTE,
    distinctChatroomCommentersCount_5_MINUTE,
    distinctChatroomAudioslotJoinCount_1_MINUTE,
    distinctChatroomAudioslotJoinCount_5_MINUTE,
    distinctChatroomAudioslotJoinCount_15_MINUTE,
    distinctChatroomAudioslotJoinCount_1_HOUR,
    distinctChatroomAudioslotJoinCount_6_HOUR,
    distinctChatroomAudioslotJoinCount_1_DAY,
    distinctChatroomAudioslotJoinCount_3_DAY,
    distinctChatroomAudioslotJoinCount_7_DAY,
    chatroomTimespentAmount_1_MINUTE,
    chatroomTimespentAmount_5_MINUTE,
    chatroomTimespentAmount_15_MINUTE,
    chatroomTimespentAmount_1_HOUR,
    chatroomTimespentAmount_6_HOUR,
    chatroomTimespentAmount_1_DAY,
    chatroomTimespentAmount_3_DAY,
    chatroomTimespentAmount_7_DAY,
    distinctChatroomSessionCount_1_MINUTE,
    distinctChatroomSessionCount_5_MINUTE,
    distinctChatroomSessionCount_15_MINUTE,
    distinctChatroomSessionCount_1_HOUR,
    distinctChatroomSessionCount_6_HOUR,
    distinctChatroomSessionCount_1_DAY,
    distinctChatroomSessionCount_3_DAY,
    distinctChatroomSessionCount_7_DAY,
    userTimespentAmount_1_DAY,
    userTimespentAmount_3_DAY,
    userTimespentAmount_7_DAY,
    userTimespentAmount_1_HOUR,
    userTimespentAmount_6_HOUR,
    userTimespentAmount_1_MINUTE,
    userTimespentAmount_5_MINUTE,
    userTimespentAmount_15_MINUTE,
    distinctUserSessionCount_1_DAY,
    distinctUserSessionCount_3_DAY,
    distinctUserSessionCount_7_DAY,
    distinctUserSessionCount_1_HOUR,
    distinctUserSessionCount_6_HOUR,
    distinctUserSessionCount_1_MINUTE,
    distinctUserSessionCount_5_MINUTE,
    distinctUserSessionCount_15_MINUTE,
    distinctUserAudioslotJoinCount_1_DAY,
    distinctUserAudioslotJoinCount_3_DAY,
    distinctUserAudioslotJoinCount_7_DAY,
    distinctUserAudioslotJoinCount_1_HOUR,
    distinctUserAudioslotJoinCount_6_HOUR,
    distinctUserAudioslotJoinCount_1_MINUTE,
    distinctUserAudioslotJoinCount_5_MINUTE,
    distinctUserAudioslotJoinCount_15_MINUTE
from ranker_features
