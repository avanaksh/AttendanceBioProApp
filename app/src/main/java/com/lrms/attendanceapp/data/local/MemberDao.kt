package com.lrms.attendanceapp.data.local

import androidx.room.*
import kotlinx.coroutines.flow.Flow

@Dao
interface MemberDao {

    @Query("SELECT * FROM members WHERE orgId = :orgId ORDER BY role DESC, id ASC")
    fun getMembersByOrg(orgId: Long): Flow<List<MemberEntity>>

    @Query("SELECT * FROM members WHERE orgId = :orgId AND role = 'ADMIN' LIMIT 1")
    suspend fun getAdminForOrg(orgId: Long): MemberEntity?

    @Query("SELECT * FROM members WHERE id = :id LIMIT 1")
    suspend fun getMemberById(id: Long): MemberEntity?

    @Query("SELECT * FROM members WHERE memberCode = :code LIMIT 1")
    suspend fun getMemberByCode(code: String): MemberEntity?

    @Query("SELECT * FROM members WHERE LOWER(memberCode) = LOWER(:identifier) OR mobile = :identifier OR LOWER(email) = LOWER(:identifier) OR aadhaarNo = :identifier LIMIT 1")
    suspend fun getMemberByIdentifier(identifier: String): MemberEntity?

    @Query("SELECT * FROM members WHERE orgId = :orgId ORDER BY role DESC, id ASC")
    suspend fun getMembersListByOrg(orgId: Long): List<MemberEntity>

    @Query("SELECT * FROM members ORDER BY orgId ASC, role DESC, id ASC")
    suspend fun getAllMembersList(): List<MemberEntity>

    @Query("SELECT COUNT(*) FROM members WHERE orgId = :orgId")
    suspend fun getMemberCount(orgId: Long): Int

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(member: MemberEntity): Long

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(members: List<MemberEntity>)

    @Update
    suspend fun update(member: MemberEntity)

    @Query("UPDATE members SET morningShiftStart = :mStart, morningShiftEnd = :mEnd, eveningShiftStart = :eStart, eveningShiftEnd = :eEnd WHERE id = :memberId")
    suspend fun updateMemberShiftTimings(memberId: Long, mStart: String, mEnd: String, eStart: String, eEnd: String)

    @Query("UPDATE members SET isBlocked = 1, blockReason = :reason WHERE memberCode = :code")
    suspend fun blockMember(code: String, reason: String)

    @Query("UPDATE members SET isBlocked = 0, blockReason = '' WHERE memberCode = :code")
    suspend fun unblockMember(code: String)

    @Query("UPDATE members SET isBlocked = 1, blockReason = :reason WHERE id = :id")
    suspend fun blockMemberById(id: Long, reason: String)

    @Query("UPDATE members SET isBlocked = 0, blockReason = '' WHERE id = :id")
    suspend fun unblockMemberById(id: Long)

    @Delete
    suspend fun delete(member: MemberEntity)
}
