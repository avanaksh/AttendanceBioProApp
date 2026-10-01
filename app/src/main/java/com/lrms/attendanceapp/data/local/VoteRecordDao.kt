package com.lrms.attendanceapp.data.local

import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Dao
interface VoteRecordDao {

    @Query("SELECT * FROM vote_records WHERE topicId = :topicId")
    fun getVotesForTopic(topicId: Long): Flow<List<VoteRecordEntity>>

    @Query("SELECT * FROM vote_records WHERE orgId = :orgId")
    fun getVotesForOrg(orgId: Long): Flow<List<VoteRecordEntity>>

    @Query("SELECT * FROM vote_records ORDER BY id DESC")
    fun getAllVotes(): Flow<List<VoteRecordEntity>>

    @Query("SELECT * FROM vote_records WHERE memberCode = :memberCode ORDER BY id DESC")
    fun getVotesForMember(memberCode: String): Flow<List<VoteRecordEntity>>

    @Query("SELECT * FROM vote_records WHERE topicId = :topicId AND memberCode = :memberCode LIMIT 1")
    suspend fun getVoteForMember(topicId: Long, memberCode: String): VoteRecordEntity?

    @Query("SELECT COUNT(*) FROM vote_records WHERE topicId = :topicId AND memberCode = :memberCode")
    suspend fun hasMemberVoted(topicId: Long, memberCode: String): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertVote(vote: VoteRecordEntity): Long

    @Query("UPDATE vote_records SET status = :status, isFinalized = :isFinalized, abandonReason = :reason WHERE id = :id")
    suspend fun updateVoteStatus(id: Long, status: String, isFinalized: Boolean, reason: String)

    @Query("UPDATE vote_records SET status = 'CONFIRMED_FINAL', isFinalized = 1 WHERE memberCode = :memberCode AND orgId = :orgId AND status = 'PENDING_EVENING_ATTENDANCE'")
    suspend fun confirmVotesForMember(memberCode: String, orgId: Long)

    @Query("UPDATE vote_records SET status = 'ABANDONED_INVALID', isFinalized = 1, abandonReason = :reason WHERE memberCode = :memberCode AND orgId = :orgId AND status = 'PENDING_EVENING_ATTENDANCE'")
    suspend fun abandonVotesForMember(memberCode: String, orgId: Long, reason: String)
}
