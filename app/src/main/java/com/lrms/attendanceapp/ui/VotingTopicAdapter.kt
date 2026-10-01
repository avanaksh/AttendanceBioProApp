package com.lrms.attendanceapp.ui

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import com.lrms.attendanceapp.data.local.VotingTopicEntity
import com.lrms.attendanceapp.databinding.ItemVotingTopicBinding

class VotingTopicAdapter(
    private var topics: List<VotingTopicEntity> = emptyList(),
    private var isAdmin: Boolean = false,
    private val onTopicClick: (VotingTopicEntity) -> Unit,
    private val onEditClick: ((VotingTopicEntity) -> Unit)? = null,
    private val onDeleteClick: ((VotingTopicEntity) -> Unit)? = null
) : RecyclerView.Adapter<VotingTopicAdapter.TopicViewHolder>() {

    private val gson = Gson()

    fun submitList(list: List<VotingTopicEntity>, adminMode: Boolean = isAdmin) {
        topics = list
        isAdmin = adminMode
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): TopicViewHolder {
        val binding = ItemVotingTopicBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return TopicViewHolder(binding)
    }

    override fun onBindViewHolder(holder: TopicViewHolder, position: Int) {
        holder.bind(topics[position])
    }

    override fun getItemCount(): Int = topics.size

    inner class TopicViewHolder(private val binding: ItemVotingTopicBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(item: VotingTopicEntity) {
            binding.tvTopicTitle.text = item.title
            binding.tvTopicDesc.text = item.description
            binding.tvTopicCategory.text = item.category
            binding.tvTopicDate.text = "📅 ${item.createdAt}"

            val period = if (item.votingStartTime.isNotEmpty() && item.votingEndTime.isNotEmpty()) {
                "⏰ Authorized Voting Period: ${item.votingStartTime} - ${item.votingEndTime} (Active only in this window)"
            } else {
                "⏰ Voting Period: 10:00 - 16:00"
            }
            binding.tvTopicVotingPeriod.text = period

            var optionsCount = 0
            try {
                val listType = object : TypeToken<List<String>>() {}.type
                val options: List<String> = gson.fromJson(item.optionsJson, listType)
                optionsCount = options.size
            } catch (_: Exception) {}

            binding.tvTopicOptionsCount.text = "🗳️ $optionsCount Options"

            // Admin edit and delete visibility
            if (isAdmin) {
                binding.btnTopicEdit.visibility = View.VISIBLE
                binding.btnTopicDelete.visibility = View.VISIBLE
            } else {
                binding.btnTopicEdit.visibility = View.GONE
                binding.btnTopicDelete.visibility = View.GONE
            }

            binding.btnTopicEdit.setOnClickListener {
                onEditClick?.invoke(item)
            }

            binding.btnTopicDelete.setOnClickListener {
                onDeleteClick?.invoke(item)
            }

            itemView.setOnClickListener {
                onTopicClick(item)
            }
            binding.btnCastVoteCta.setOnClickListener {
                onTopicClick(item)
            }
        }
    }
}
