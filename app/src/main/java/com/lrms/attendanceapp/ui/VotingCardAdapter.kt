package com.lrms.attendanceapp.ui

import android.view.LayoutInflater
import android.view.ViewGroup
import android.widget.Button
import android.widget.TextView
import androidx.core.content.ContextCompat
import androidx.recyclerview.widget.RecyclerView
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import com.lrms.attendanceapp.R
import com.lrms.attendanceapp.data.local.VoteRecordEntity
import com.lrms.attendanceapp.data.local.VotingTopicEntity
import com.lrms.attendanceapp.databinding.ItemVotingCardBinding
import java.util.Calendar

class VotingCardAdapter(
    private var topics: List<VotingTopicEntity> = emptyList(),
    private var votesMap: Map<Long, List<VoteRecordEntity>> = emptyMap(),
    private var userVotedMap: Map<Long, VoteRecordEntity> = emptyMap(),
    private var isMorningAttendanceMarked: Boolean = true,
    private val onCastVote: (VotingTopicEntity, String) -> Unit
) : RecyclerView.Adapter<VotingCardAdapter.BallotViewHolder>() {

    private val gson = Gson()

    fun updateData(
        newTopics: List<VotingTopicEntity>,
        newVotesMap: Map<Long, List<VoteRecordEntity>>,
        newUserVotedMap: Map<Long, VoteRecordEntity>,
        morningMarked: Boolean = isMorningAttendanceMarked
    ) {
        topics = newTopics
        votesMap = newVotesMap
        userVotedMap = newUserVotedMap
        isMorningAttendanceMarked = morningMarked
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): BallotViewHolder {
        val binding = ItemVotingCardBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return BallotViewHolder(binding)
    }

    override fun onBindViewHolder(holder: BallotViewHolder, position: Int) {
        holder.bind(topics[position])
    }

    override fun getItemCount(): Int = topics.size

    inner class BallotViewHolder(private val binding: ItemVotingCardBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(item: VotingTopicEntity) {
            val context = itemView.context
            binding.tvBallotTitle.text = item.title
            binding.tvBallotDesc.text = item.description
            binding.tvBallotCategory.text = item.category

            val startTime = if (item.votingStartTime.isNotEmpty()) item.votingStartTime else "10:00"
            val endTime = if (item.votingEndTime.isNotEmpty()) item.votingEndTime else "16:00"
            val inPeriod = isCurrentTimeInPeriod(startTime, endTime)

            if (inPeriod) {
                binding.tvBallotVotingPeriod.text = "⏰ Authorized Voting Window: $startTime - $endTime (ACTIVE NOW)"
                binding.tvBallotVotingPeriod.setBackgroundResource(R.drawable.bg_pill_emerald)
                binding.tvBallotVotingPeriod.setTextColor(ContextCompat.getColor(context, R.color.emerald_500))
            } else {
                binding.tvBallotVotingPeriod.text = "⏰ Authorized Voting Window: $startTime - $endTime (LOCKED OUTSIDE WINDOW)"
                binding.tvBallotVotingPeriod.setBackgroundResource(R.drawable.bg_pill_amber)
                binding.tvBallotVotingPeriod.setTextColor(ContextCompat.getColor(context, R.color.amber_500))
            }

            val topicVotes = votesMap[item.id] ?: emptyList()
            val totalVotes = topicVotes.count { it.status != VoteRecordEntity.STATUS_ABANDONED }
            val userVote = userVotedMap[item.id]

            if (userVote != null) {
                binding.tvBallotVotedBadge.visibility = android.view.View.VISIBLE
                when (userVote.status) {
                    VoteRecordEntity.STATUS_CONFIRMED -> {
                        binding.tvBallotVotedBadge.text = "✓ Confirmed: ${userVote.selectedOption}"
                        binding.tvBallotVotedBadge.setBackgroundResource(R.drawable.bg_pill_emerald)
                        binding.tvBallotVotedBadge.setTextColor(ContextCompat.getColor(context, R.color.emerald_500))
                    }
                    VoteRecordEntity.STATUS_ABANDONED -> {
                        binding.tvBallotVotedBadge.text = "❌ ABANDONED (Duty Absent)"
                        binding.tvBallotVotedBadge.setBackgroundResource(R.drawable.bg_pill_rose)
                        binding.tvBallotVotedBadge.setTextColor(ContextCompat.getColor(context, R.color.rose_500))
                    }
                    else -> {
                        binding.tvBallotVotedBadge.text = "⏳ Voted: ${userVote.selectedOption} (Pending Evening Attendance)"
                        binding.tvBallotVotedBadge.setBackgroundResource(R.drawable.bg_pill_amber)
                        binding.tvBallotVotedBadge.setTextColor(ContextCompat.getColor(context, R.color.amber_500))
                    }
                }
            } else {
                binding.tvBallotVotedBadge.visibility = android.view.View.GONE
            }

            binding.tvBallotTally.text = "Total Valid Ballots Cast: $totalVotes"

            // Parse options
            var optionsList: List<String> = emptyList()
            try {
                val listType = object : TypeToken<List<String>>() {}.type
                optionsList = gson.fromJson(item.optionsJson, listType)
            } catch (_: Exception) {}

            binding.llOptionsContainer.removeAllViews()

            for (option in optionsList) {
                val count = topicVotes.count { it.selectedOption == option && it.status != VoteRecordEntity.STATUS_ABANDONED }
                val percent = if (totalVotes > 0) (count * 100) / totalVotes else 0

                val optionView = LayoutInflater.from(context).inflate(
                    R.layout.item_voting_option_row,
                    binding.llOptionsContainer,
                    false
                )

                val tvOptionTitle = optionView.findViewById<TextView>(R.id.tv_option_title)
                val tvOptionCount = optionView.findViewById<TextView>(R.id.tv_option_count)
                val btnVote = optionView.findViewById<Button>(R.id.btn_cast_option_vote)

                tvOptionTitle.text = option
                tvOptionCount.text = "$count votes ($percent%)"

                if (userVote != null) {
                    btnVote.isEnabled = false
                    if (userVote.selectedOption == option) {
                        btnVote.text = if (userVote.status == VoteRecordEntity.STATUS_ABANDONED) "Abandoned" else "Voted ✓"
                        btnVote.setBackgroundColor(
                            ContextCompat.getColor(
                                context,
                                if (userVote.status == VoteRecordEntity.STATUS_ABANDONED) R.color.rose_500 else R.color.emerald_500
                            )
                        )
                    } else {
                        btnVote.text = "Recorded"
                        btnVote.alpha = 0.4f
                    }
                } else if (!isMorningAttendanceMarked) {
                    btnVote.isEnabled = false
                    btnVote.text = "Morning Required"
                    btnVote.alpha = 0.4f
                } else if (!inPeriod) {
                    btnVote.isEnabled = false
                    btnVote.text = "Outside Window"
                    btnVote.alpha = 0.4f
                } else {
                    btnVote.isEnabled = true
                    btnVote.text = "Cast Vote"
                    btnVote.alpha = 1.0f
                    btnVote.setOnClickListener {
                        onCastVote(item, option)
                    }
                }

                binding.llOptionsContainer.addView(optionView)
            }
        }

        private fun isCurrentTimeInPeriod(startStr: String, endStr: String): Boolean {
            try {
                val cal = Calendar.getInstance()
                val nowMinutes = cal.get(Calendar.HOUR_OF_DAY) * 60 + cal.get(Calendar.MINUTE)

                val sParts = startStr.split(":").map { it.trim().toInt() }
                val eParts = endStr.split(":").map { it.trim().toInt() }

                val startMin = sParts[0] * 60 + (if (sParts.size > 1) sParts[1] else 0)
                val endMin = eParts[0] * 60 + (if (eParts.size > 1) eParts[1] else 0)

                return nowMinutes in startMin..endMin
            } catch (_: Exception) {
                return true
            }
        }
    }
}
