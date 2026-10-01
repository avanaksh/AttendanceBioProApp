package com.lrms.attendanceapp.data.local

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "voting_topics")
data class VotingTopicEntity(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,
    val orgId: Long,
    val title: String,
    val description: String,
    val category: String, // "Topic", "Problem", "Issue", "Notification", "Announcement", "Election"
    val optionsJson: String, // JSON array of options e.g. ["Adv. Rajeshwar Sharma", "Justice P. K. Sen"]
    val createdBy: String = "Administrator",
    val createdAt: String,
    val isActive: Boolean = true,
    var votingStartTime: String = "10:00", // HH:mm
    var votingEndTime: String = "16:00",   // HH:mm
    var votingDate: String = ""            // e.g. "30/09/2026"
)
