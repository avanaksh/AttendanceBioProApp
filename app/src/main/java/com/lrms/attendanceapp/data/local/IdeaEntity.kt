package com.lrms.attendanceapp.data.local

import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Entity(tableName = "local_ideas")
data class IdeaEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val title: String,
    val category: String,
    val description: String,
    val createdAt: String,
    var isSynced: Boolean = false
)

@Dao
interface IdeaDao {
    @Query("SELECT * FROM local_ideas ORDER BY id DESC")
    fun getAllIdeas(): Flow<List<IdeaEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertIdea(idea: IdeaEntity): Long
}
