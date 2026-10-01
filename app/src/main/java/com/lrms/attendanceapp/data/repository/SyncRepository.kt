package com.lrms.attendanceapp.data.repository

import com.lrms.attendanceapp.data.local.AttendanceDao
import com.lrms.attendanceapp.data.local.AttendanceEntity
import com.lrms.attendanceapp.data.remote.ApiService
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class SyncRepository(
    private val attendanceDao: AttendanceDao,
    private val apiService: ApiService
) {

    suspend fun saveLogLocally(log: AttendanceEntity): Long {
        return withContext(Dispatchers.IO) {
            attendanceDao.insertLog(log)
        }
    }

    suspend fun syncUnsyncedLogsToCloudServer(): Int {
        return withContext(Dispatchers.IO) {
            val unsyncedList = attendanceDao.getUnsyncedLogs()
            var successCount = 0

            for (log in unsyncedList) {
                try {
                    val response = apiService.syncAttendanceLog(log)
                    if (response.isSuccessful) {
                        attendanceDao.markSynced(log.id)
                        successCount++
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }

            successCount
        }
    }
}
