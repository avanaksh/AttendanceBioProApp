package com.lrms.attendanceapp.data.local

import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Dao
interface VotingTopicDao {

    @Query("SELECT * FROM voting_topics WHERE orgId = :orgId AND isActive = 1 ORDER BY id DESC")
    fun getTopicsForOrg(orgId: Long): Flow<List<VotingTopicEntity>>

    @Query("SELECT * FROM voting_topics WHERE id = :id LIMIT 1")
    suspend fun getTopicById(id: Long): VotingTopicEntity?

    @Query("SELECT COUNT(*) FROM voting_topics WHERE orgId = :orgId AND isActive = 1")
    suspend fun getActiveTopicCount(orgId: Long): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(topic: VotingTopicEntity): Long

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(topics: List<VotingTopicEntity>)

    @Update
    suspend fun update(topic: VotingTopicEntity)

    @Delete
    suspend fun delete(topic: VotingTopicEntity)

    @Query("DELETE FROM voting_topics WHERE id = :id")
    suspend fun deleteById(id: Long)

    @Query("UPDATE voting_topics SET title = :title, description = :description, category = :category, optionsJson = :optionsJson, votingStartTime = :startTime, votingEndTime = :endTime WHERE id = :id")
    suspend fun updateTopicDetails(id: Long, title: String, description: String, category: String, optionsJson: String, startTime: String, endTime: String)
}
