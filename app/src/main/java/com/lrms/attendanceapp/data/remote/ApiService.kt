package com.lrms.attendanceapp.data.remote

import com.lrms.attendanceapp.data.local.AttendanceEntity
import com.lrms.attendanceapp.data.local.IdeaEntity
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Query

data class LoginRequestDto(
    val emailOrMobileOrAadhaar: String,
    val password: String
)

data class UserResponseDto(
    val success: Boolean,
    val userId: String,
    val userName: String,
    val userEmail: String,
    val mobileNo: String,
    val aadhaarNo: String,
    val state: String,
    val district: String,
    val instituteName: String,
    val instituteId: String,
    val role: String,
    val message: String?
)

data class VoteRequestDto(
    val userId: String,
    val candidateId: Int,
    val candidateName: String,
    val partyName: String,
    val state: String,
    val district: String,
    val latitude: String,
    val longitude: String
)

data class ApiResponseDto(
    val success: Boolean,
    val message: String
)

interface ApiService {

    @POST("api/auth/login")
    suspend fun login(@Body req: LoginRequestDto): Response<UserResponseDto>

    @POST("api/attendance")
    suspend fun syncAttendanceLog(@Body log: AttendanceEntity): Response<ApiResponseDto>

    @POST("api/ideas")
    suspend fun syncIdea(@Body idea: IdeaEntity): Response<ApiResponseDto>

    @POST("api/voting/cast")
    suspend fun castVote(@Body req: VoteRequestDto): Response<ApiResponseDto>
}
