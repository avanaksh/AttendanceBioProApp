package com.lrms.attendanceapp.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "members")
data class MemberEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val orgId: Long,
    val memberCode: String, // e.g. "ADM-001", "MEM-101"
    val name: String,
    val role: String, // "ADMIN" or "MEMBER"
    val natureOfWork: String, // Designation/Duty (e.g. "Presiding Judge", "Court Registrar", "Chief Engineer", "Ward Councilor", "President", "Secretary", etc.)
    val mobile: String,
    val email: String,
    val aadhaarNo: String = "",
    var morningShiftStart: String = "", // If empty, inherits from organization
    var morningShiftEnd: String = "",
    var eveningShiftStart: String = "",
    var eveningShiftEnd: String = "",
    var isBlocked: Boolean = false,
    var blockReason: String = ""
)
