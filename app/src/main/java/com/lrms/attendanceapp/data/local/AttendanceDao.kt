package com.lrms.attendanceapp.data.local

import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Dao
interface AttendanceDao {

    @Query("SELECT * FROM local_attendance_logs ORDER BY id DESC")
    fun getAllLogs(): Flow<List<AttendanceEntity>>

    @Query("SELECT * FROM local_attendance_logs WHERE userId = :userId ORDER BY id DESC")
    fun getLogsByUserId(userId: String): Flow<List<AttendanceEntity>>

    @Query("SELECT * FROM local_attendance_logs WHERE userId = :identifier OR aadhaarNo = :identifier OR mobileNo = :identifier OR userEmail = :identifier OR memberCode = :identifier ORDER BY id DESC")
    fun getLogsForUser(identifier: String): Flow<List<AttendanceEntity>>

    @Query("SELECT * FROM local_attendance_logs WHERE orgId = :orgId ORDER BY id DESC")
    fun getLogsForOrg(orgId: Long): Flow<List<AttendanceEntity>>

    @Query("SELECT * FROM local_attendance_logs WHERE orgId = :orgId AND (memberCode = :memberCode OR userId = :memberCode) ORDER BY id DESC")
    fun getLogsForMember(orgId: Long, memberCode: String): Flow<List<AttendanceEntity>>

    @Query("SELECT * FROM local_attendance_logs WHERE isSynced = 0")
    suspend fun getUnsyncedLogs(): List<AttendanceEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertLog(log: AttendanceEntity): Long

    @Query("UPDATE local_attendance_logs SET isSynced = 1 WHERE id = :id")
    suspend fun markSynced(id: Long)

    @Query("DELETE FROM local_attendance_logs")
    suspend fun clearAll()
}
