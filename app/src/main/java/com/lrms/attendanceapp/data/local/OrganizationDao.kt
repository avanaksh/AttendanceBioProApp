package com.lrms.attendanceapp.data.local

import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Dao
interface OrganizationDao {

    @Query("SELECT * FROM organizations ORDER BY id ASC")
    fun getAllOrganizations(): Flow<List<OrganizationEntity>>

    @Query("SELECT * FROM organizations ORDER BY id ASC")
    suspend fun getAllOrganizationsList(): List<OrganizationEntity>

    @Query("SELECT * FROM organizations WHERE id = :id LIMIT 1")
    suspend fun getOrganizationById(id: Long): OrganizationEntity?

    @Query("SELECT COUNT(*) FROM organizations")
    suspend fun getCount(): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(organization: OrganizationEntity): Long

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(organizations: List<OrganizationEntity>)

    @Update
    suspend fun update(organization: OrganizationEntity)

    @Query("UPDATE organizations SET morningShiftStart = :mStart, morningShiftEnd = :mEnd, eveningShiftStart = :eStart, eveningShiftEnd = :eEnd WHERE id = :orgId")
    suspend fun updateShiftTimings(orgId: Long, mStart: String, mEnd: String, eStart: String, eEnd: String)
}
