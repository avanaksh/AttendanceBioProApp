package com.lrms.attendanceapp.ui

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.lrms.attendanceapp.data.local.OrganizationEntity
import com.lrms.attendanceapp.databinding.ItemOrganizationBinding

class OrganizationAdapter(
    private var organizations: List<OrganizationEntity> = emptyList(),
    private val onItemClick: (OrganizationEntity) -> Unit
) : RecyclerView.Adapter<OrganizationAdapter.OrgViewHolder>() {

    fun submitList(list: List<OrganizationEntity>) {
        organizations = list
        notifyDataSetChanged()
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): OrgViewHolder {
        val binding = ItemOrganizationBinding.inflate(
            LayoutInflater.from(parent.context),
            parent,
            false
        )
        return OrgViewHolder(binding)
    }

    override fun onBindViewHolder(holder: OrgViewHolder, position: Int) {
        holder.bind(organizations[position])
    }

    override fun getItemCount(): Int = organizations.size

    inner class OrgViewHolder(private val binding: ItemOrganizationBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(item: OrganizationEntity) {
            binding.tvOrgName.text = item.name
            binding.tvOrgCategory.text = item.category
            binding.tvOrgPurpose.text = "🎯 Purpose: ${item.purpose}"
            binding.tvOrgShifts.text = "⏱️ Shifts: ${item.morningShiftStart} - ${item.morningShiftEnd} | ${item.eveningShiftStart} - ${item.eveningShiftEnd}"

            val icon = when (item.code) {
                "SC_HC" -> "⚖️"
                "MUNICIPAL" -> "🏛️"
                "STATE_UT" -> "🌾"
                "HOUSING_SOC" -> "🏘️"
                "INSTITUTE" -> "🎓"
                "ELECTION_AUTH" -> "🗳️"
                else -> "🏢"
            }
            binding.tvOrgIcon.text = icon

            itemView.setOnClickListener {
                onItemClick(item)
            }
        }
    }
}
