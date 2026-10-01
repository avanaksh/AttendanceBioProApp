package com.lrms.attendanceapp.ui

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.DiffUtil
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.lrms.attendanceapp.R
import com.lrms.attendanceapp.data.local.AttendanceEntity
import com.lrms.attendanceapp.databinding.ItemAttendanceRecordBinding

class AdminAttendanceAdapter : ListAdapter<AttendanceEntity, AdminAttendanceAdapter.RecordViewHolder>(DiffCallback) {

    var onItemClickListener: ((AttendanceEntity) -> Unit)? = null

    inner class RecordViewHolder(private val binding: ItemAttendanceRecordBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(item: AttendanceEntity) {
            binding.root.setOnClickListener {
                onItemClickListener?.invoke(item)
            }
            binding.tvRecordName.text = item.userName
            binding.tvRecordUserid.text = "ID: ${item.userId} | ${item.instituteName}"
            binding.tvRecordOccasion.text = "Occasion: ${item.occasion}"
            binding.tvRecordAadhaar.text = item.aadhaarNo
            binding.tvRecordTimestamp.text = item.timestamp
            binding.tvRecordVerification.text = "${item.verificationMode} (Confidence: ${item.confidence})"
            binding.tvRecordLocation.text = "${item.address} (${item.latitude}, ${item.longitude})"

            // Type Badge Styling
            val displayType = when {
                item.attendanceType.contains("Morning", ignoreCase = true) -> "Morning Shift"
                item.attendanceType.contains("Evening", ignoreCase = true) -> "Evening Shift"
                else -> item.attendanceType
            }
            binding.tvRecordTypeBadge.text = displayType
            if (item.attendanceType.contains("Vote", ignoreCase = true) || item.occasion.contains("Election", ignoreCase = true)) {
                binding.tvRecordTypeBadge.setBackgroundColor(ContextCompat.getColor(binding.root.context, R.color.emerald_500))
            } else if (item.attendanceType.contains("Morning", ignoreCase = true)) {
                binding.tvRecordTypeBadge.setBackgroundResource(R.drawable.bg_btn_indigo)
            } else {
                binding.tvRecordTypeBadge.setBackgroundResource(R.drawable.bg_badge_gold)
            }

            binding.tvRecordSyncStatus.visibility = View.GONE
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecordViewHolder {
        val binding = ItemAttendanceRecordBinding.inflate(
            LayoutInflater.from(parent.context), parent, false
        )
        return RecordViewHolder(binding)
    }

    override fun onBindViewHolder(holder: RecordViewHolder, position: Int) {
        holder.bind(getItem(position))
    }

    companion object DiffCallback : DiffUtil.ItemCallback<AttendanceEntity>() {
        override fun areItemsTheSame(oldItem: AttendanceEntity, newItem: AttendanceEntity): Boolean {
            return oldItem.id == newItem.id
        }

        override fun areContentsTheSame(oldItem: AttendanceEntity, newItem: AttendanceEntity): Boolean {
            return oldItem == newItem
        }
    }
}
