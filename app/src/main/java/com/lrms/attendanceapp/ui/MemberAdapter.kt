package com.lrms.attendanceapp.ui

import android.content.res.ColorStateList
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.RecyclerView
import com.lrms.attendanceapp.R
import com.lrms.attendanceapp.data.local.MemberEntity
import com.lrms.attendanceapp.data.local.VoteRecordEntity
import com.lrms.attendanceapp.databinding.ItemMemberBinding

class MemberAdapter(
    private var members: List<MemberEntity> = emptyList(),
    private var defaultShiftHours: String = "09:00 - 13:00 | 16:00 - 19:00",
    private var attendanceStatusMap: Map<String, Pair<Boolean, Boolean>> = emptyMap(),
    private var memberVoteMap: Map<String, VoteRecordEntity> = emptyMap(),
    private val onLoginClick: (MemberEntity) -> Unit,
    private val onOptionsClick: (MemberEntity) -> Unit
) : RecyclerView.Adapter<MemberAdapter.MemberViewHolder>() {

    fun updateData(
        newMembers: List<MemberEntity>,
        newDefaultShiftHours: String,
        newStatusMap: Map<String, Pair<Boolean, Boolean>>,
        newVoteMap: Map<String, VoteRecordEntity> = emptyMap()
    ) {
        members = newMembers
        defaultShiftHours = newDefaultShiftHours
        attendanceStatusMap = newStatusMap
        memberVoteMap = newVoteMap
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): MemberViewHolder {
        val binding = ItemMemberBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return MemberViewHolder(binding)
    }

    override fun onBindViewHolder(holder: MemberViewHolder, position: Int) {
        holder.bind(members[position])
    }

    override fun getItemCount(): Int = members.size

    inner class MemberViewHolder(private val binding: ItemMemberBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(item: MemberEntity) {
            val context = itemView.context
            binding.tvMemberName.text = item.name
            binding.tvMemberWork.text = "Nature of Work: ${item.natureOfWork}"

            // Avatar Initials
            val words = item.name.split(" ").filter { it.isNotBlank() }
            val initials = if (words.size >= 2) {
                "${words[0].first()}${words[1].first()}".uppercase()
            } else if (words.isNotEmpty()) {
                words[0].take(2).uppercase()
            } else {
                "ME"
            }
            binding.tvMemberAvatar.text = initials

            // Role Badge
            val isAdmin = item.role.equals("ADMIN", ignoreCase = true)
            if (isAdmin) {
                binding.tvMemberRoleBadge.text = "👑 ADMIN"
                binding.tvMemberRoleBadge.setBackgroundResource(R.drawable.bg_badge_gold)
                binding.tvMemberRoleBadge.setTextColor(ContextCompat.getColor(context, R.color.slate_950))
            } else {
                binding.tvMemberRoleBadge.text = "MEMBER"
                binding.tvMemberRoleBadge.setBackgroundResource(R.drawable.bg_pill_role)
                binding.tvMemberRoleBadge.setTextColor(ContextCompat.getColor(context, R.color.white))
            }

            if (item.isBlocked) {
                binding.tvMemberBlockedBadge.visibility = View.VISIBLE
                binding.tvMemberBlockReason.visibility = View.VISIBLE
                binding.tvMemberBlockReason.text = "🚨 Blocked: ${item.blockReason.ifEmpty { "Discrepancy Found in Duty/Vote" }}"
            } else {
                binding.tvMemberBlockedBadge.visibility = View.GONE
                binding.tvMemberBlockReason.visibility = View.GONE
            }

            // Shift Hours
            val mHours = if (item.morningShiftStart.isNotEmpty() && item.morningShiftEnd.isNotEmpty()) {
                "${item.morningShiftStart} - ${item.morningShiftEnd} | ${item.eveningShiftStart} - ${item.eveningShiftEnd}"
            } else {
                defaultShiftHours
            }
            binding.tvShiftHoursDisplay.text = "⏱️ Hours: $mHours"

            // Today's attendance status
            val status = attendanceStatusMap[item.memberCode] ?: Pair(false, false)
            val hasMorning = status.first
            val hasEvening = status.second

            if (hasMorning) {
                binding.tvMorningStatus.text = "Morning ✓"
                binding.tvMorningStatus.setBackgroundResource(R.drawable.bg_pill_emerald)
                binding.tvMorningStatus.setTextColor(ContextCompat.getColor(context, R.color.emerald_500))
            } else {
                binding.tvMorningStatus.text = "Morning ⏳"
                binding.tvMorningStatus.setBackgroundResource(R.drawable.bg_pill_amber)
                binding.tvMorningStatus.setTextColor(ContextCompat.getColor(context, R.color.amber_500))
            }

            if (hasEvening) {
                binding.tvEveningStatus.text = "Evening ✓"
                binding.tvEveningStatus.setBackgroundResource(R.drawable.bg_pill_emerald)
                binding.tvEveningStatus.setTextColor(ContextCompat.getColor(context, R.color.emerald_500))
            } else {
                binding.tvEveningStatus.text = "Evening ⏳"
                binding.tvEveningStatus.setBackgroundResource(R.drawable.bg_pill_amber)
                binding.tvEveningStatus.setTextColor(ContextCompat.getColor(context, R.color.amber_500))
            }

            // Today's voting & duty validation status: 👍 Thumbs Up vs 👎 Thumbs Down
            val vote = memberVoteMap[item.memberCode]
            val isProperlyValidated = hasMorning && vote != null && (vote.status == VoteRecordEntity.STATUS_CONFIRMED || hasEvening)

            if (isProperlyValidated) {
                // Morning + Vote Cast + Evening ALL DONE and Validated -> THUMBS UP 👍
                binding.tvMemberVoteStatus.text = "👍 VALIDATED and COUNTED ✓ (${vote?.selectedOption})"
                binding.tvMemberVoteStatus.setBackgroundResource(R.drawable.bg_pill_emerald)
                binding.tvMemberVoteStatus.setTextColor(ContextCompat.getColor(context, R.color.emerald_500))
            } else {
                // Incomplete or discrepancy -> THUMBS DOWN 👎
                binding.tvMemberVoteStatus.setBackgroundResource(R.drawable.bg_pill_rose)
                binding.tvMemberVoteStatus.setTextColor(ContextCompat.getColor(context, R.color.rose_500))

                if (item.isBlocked) {
                    binding.tvMemberVoteStatus.text = "👎 BLOCKED: Discrepancy Found"
                } else if (!hasMorning) {
                    binding.tvMemberVoteStatus.text = "👎 INCOMPLETE: Morning Shift Missing"
                } else if (vote == null) {
                    binding.tvMemberVoteStatus.text = "👎 INCOMPLETE: Vote Not Cast"
                } else {
                    // Morning done + Vote done, but Evening is missing!
                    binding.tvMemberVoteStatus.text = "👎 UNCOUNTED: Evening Shift Absent (${vote.selectedOption})"
                }
            }

            // Direct Login Button Configuration
            if (item.isBlocked) {
                binding.btnMemberLogin.text = "🚨 Blocked"
                binding.btnMemberLogin.backgroundTintList = ColorStateList.valueOf(ContextCompat.getColor(context, R.color.rose_500))
                binding.btnMemberLogin.setTextColor(ContextCompat.getColor(context, R.color.white))
            } else {
                binding.btnMemberLogin.text = "Login"
                binding.btnMemberLogin.backgroundTintList = ColorStateList.valueOf(ContextCompat.getColor(context, if (isAdmin) R.color.amber_500 else R.color.indigo_600))
                binding.btnMemberLogin.setTextColor(ContextCompat.getColor(context, if (isAdmin) R.color.slate_950 else R.color.white))
            }

            binding.btnMemberLogin.setOnClickListener {
                onLoginClick(item)
            }

            binding.ibMemberOptions.setOnClickListener {
                onOptionsClick(item)
            }

            itemView.setOnClickListener {
                onLoginClick(item)
            }
        }
    }
}
