package com.lrms.attendanceapp.data.local

import android.content.Context
import androidx.room.Database
import androidx.room.Room
import androidx.room.RoomDatabase

@Database(
    entities = [
        AttendanceEntity::class,
        IdeaEntity::class,
        OrganizationEntity::class,
        MemberEntity::class,
        VotingTopicEntity::class,
        VoteRecordEntity::class
    ],
    version = 4,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {

    abstract fun attendanceDao(): AttendanceDao
    abstract fun ideaDao(): IdeaDao
    abstract fun organizationDao(): OrganizationDao
    abstract fun memberDao(): MemberDao
    abstract fun votingTopicDao(): VotingTopicDao
    abstract fun voteRecordDao(): VoteRecordDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "biocheck_local.db"
                ).fallbackToDestructiveMigration()
                 .build()
                INSTANCE = instance
                DatabaseInitializer.populateInitialDataIfNeeded(instance)
                instance
            }
        }
    }
}
