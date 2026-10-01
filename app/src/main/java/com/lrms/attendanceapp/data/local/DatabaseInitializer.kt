package com.lrms.attendanceapp.data.local

import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

object DatabaseInitializer {

    fun populateInitialDataIfNeeded(database: AppDatabase) {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val db = database.openHelper.writableDatabase
                db.execSQL("UPDATE organizations SET name = REPLACE(name, '&', 'and'), purpose = REPLACE(purpose, '&', 'and') WHERE name LIKE '%&%' OR purpose LIKE '%&%'")
                db.execSQL("UPDATE members SET natureOfWork = REPLACE(natureOfWork, '&', 'and') WHERE natureOfWork LIKE '%&%'")
                db.execSQL("UPDATE voting_topics SET title = REPLACE(title, '&', 'and'), optionsJson = REPLACE(optionsJson, '&', 'and') WHERE title LIKE '%&%' OR optionsJson LIKE '%&%'")
            } catch (_: Exception) {}

            if (database.organizationDao().getCount() > 0) {
                return@launch
            }

            val todayDate = SimpleDateFormat("dd/MM/yyyy", Locale.getDefault()).format(Date())

            // 1. SC / HC
            val scHcId = database.organizationDao().insert(
                OrganizationEntity(
                    name = "Supreme Court and High Court (Judiciary)",
                    code = "SC_HC",
                    category = "SC/HC",
                    purpose = "Cast vote for Selection of Judges/CJM/DJM",
                    iconType = "court",
                    morningShiftStart = "09:00",
                    morningShiftEnd = "13:00",
                    eveningShiftStart = "15:30",
                    eveningShiftEnd = "18:30"
                )
            )

            // 1 Admin + 10 Members for SC/HC
            database.memberDao().insertAll(
                listOf(
                    MemberEntity(orgId = scHcId, memberCode = "JUD-ADM-01", name = "Hon. Justice D. Y. Chandramohan", role = "ADMIN", natureOfWork = "Chief Administrative Judge and Bench In-charge", mobile = "9820011221", email = "chief.justice@judiciary.gov.in", aadhaarNo = "9012-3456-7890"),
                    MemberEntity(orgId = scHcId, memberCode = "JUD-MEM-01", name = "Justice S. Ravindra Bhattacharya", role = "MEMBER", natureOfWork = "High Court Senior Presiding Judge", mobile = "9820011222", email = "justice.srb@judiciary.gov.in", aadhaarNo = "9012-3456-7891"),
                    MemberEntity(orgId = scHcId, memberCode = "JUD-MEM-02", name = "Adv. Rajeshwar Sharma", role = "MEMBER", natureOfWork = "Chief Judicial Magistrate (CJM)", mobile = "9820011223", email = "cjm.sharma@judiciary.gov.in", aadhaarNo = "9012-3456-7892"),
                    MemberEntity(orgId = scHcId, memberCode = "JUD-MEM-03", name = "Adv. Meenakshi Sundaram", role = "MEMBER", natureOfWork = "District Judicial Magistrate (DJM)", mobile = "9820011224", email = "djm.meenakshi@judiciary.gov.in", aadhaarNo = "9012-3456-7893"),
                    MemberEntity(orgId = scHcId, memberCode = "JUD-MEM-04", name = "Shri Anand Vardhan", role = "MEMBER", natureOfWork = "Court Registrar General", mobile = "9820011225", email = "registrar@judiciary.gov.in", aadhaarNo = "9012-3456-7894"),
                    MemberEntity(orgId = scHcId, memberCode = "JUD-MEM-05", name = "Smt. Priyanka Solanki", role = "MEMBER", natureOfWork = "Senior Judicial Bench Clerk", mobile = "9820011226", email = "clerk.solanki@judiciary.gov.in", aadhaarNo = "9012-3456-7895"),
                    MemberEntity(orgId = scHcId, memberCode = "JUD-MEM-06", name = "Adv. Harish Salvekar", role = "MEMBER", natureOfWork = "Bar Council Liaison Advocate", mobile = "9820011227", email = "adv.harish@judiciary.gov.in", aadhaarNo = "9012-3456-7896"),
                    MemberEntity(orgId = scHcId, memberCode = "JUD-MEM-07", name = "Vikramaditya Roy", role = "MEMBER", natureOfWork = "Court Protocol Officer", mobile = "9820011228", email = "protocol.roy@judiciary.gov.in", aadhaarNo = "9012-3456-7897"),
                    MemberEntity(orgId = scHcId, memberCode = "JUD-MEM-08", name = "Sunita Deshmukh", role = "MEMBER", natureOfWork = "Case Scrutiny and Filing Officer", mobile = "9820011229", email = "scrutiny.deshmukh@judiciary.gov.in", aadhaarNo = "9012-3456-7898"),
                    MemberEntity(orgId = scHcId, memberCode = "JUD-MEM-09", name = "Arjun Nair", role = "MEMBER", natureOfWork = "Judicial IT Infrastructure Engineer", mobile = "9820011230", email = "it.nair@judiciary.gov.in", aadhaarNo = "9012-3456-7899"),
                    MemberEntity(orgId = scHcId, memberCode = "JUD-MEM-10", name = "Kavita Menon", role = "MEMBER", natureOfWork = "Judicial Record Room Supervisor", mobile = "9820011231", email = "records.menon@judiciary.gov.in", aadhaarNo = "9012-3456-7800")
                )
            )

            // Topic for SC/HC
            database.votingTopicDao().insert(
                VotingTopicEntity(
                    orgId = scHcId,
                    title = "Selection of Judicial Panel: CJM and DJM Appointments 2026",
                    description = "Official collegium election for selecting candidates to the Chief Judicial Magistrate (CJM) and District Judicial Magistrate (DJM) panels.",
                    category = "Judicial Election Notification",
                    optionsJson = "[\"Adv. Rajeshwar Sharma (CJM Panel)\", \"Adv. Meenakshi Sundaram (DJM Panel)\", \"Adv. K. R. Nambiar (Senior Judicial Panel)\"]",
                    createdAt = todayDate
                )
            )

            // 2. Municipal Corporation
            val mcId = database.organizationDao().insert(
                OrganizationEntity(
                    name = "Greater Municipal Corporation",
                    code = "MUNICIPAL",
                    category = "Municipal Corporation",
                    purpose = "Caste vote for Nigam Parishad",
                    iconType = "municipal",
                    morningShiftStart = "08:30",
                    morningShiftEnd = "12:30",
                    eveningShiftStart = "15:00",
                    eveningShiftEnd = "18:00"
                )
            )

            // 1 Admin + 10 Members for Municipal Corporation
            database.memberDao().insertAll(
                listOf(
                    MemberEntity(orgId = mcId, memberCode = "MC-ADM-01", name = "Commissioner Rajiv Ranjan IAS", role = "ADMIN", natureOfWork = "Municipal Commissioner and Returning Officer", mobile = "9830022331", email = "commissioner@mc.gov.in", aadhaarNo = "8012-3456-7890"),
                    MemberEntity(orgId = mcId, memberCode = "MC-MEM-01", name = "Sunil Ghadge", role = "MEMBER", natureOfWork = "Elected Ward Councilor (Ward 14)", mobile = "9830022332", email = "ward14@mc.gov.in", aadhaarNo = "8012-3456-7891"),
                    MemberEntity(orgId = mcId, memberCode = "MC-MEM-02", name = "Anita Sawant", role = "MEMBER", natureOfWork = "Nigam Parishad Executive Delegate", mobile = "9830022333", email = "anita.sawant@mc.gov.in", aadhaarNo = "8012-3456-7892"),
                    MemberEntity(orgId = mcId, memberCode = "MC-MEM-03", name = "Mohanlal Soni", role = "MEMBER", natureOfWork = "Chief Municipal Civil Engineer", mobile = "9830022334", email = "engineer.soni@mc.gov.in", aadhaarNo = "8012-3456-7893"),
                    MemberEntity(orgId = mcId, memberCode = "MC-MEM-04", name = "Geeta Bhardwaj", role = "MEMBER", natureOfWork = "Chief Sanitation and Waste Supervisor", mobile = "9830022335", email = "sanitation.bhardwaj@mc.gov.in", aadhaarNo = "8012-3456-7894"),
                    MemberEntity(orgId = mcId, memberCode = "MC-MEM-05", name = "Prakash Jadhav", role = "MEMBER", natureOfWork = "Property Tax and Revenue Assessor", mobile = "9830022336", email = "revenue.jadhav@mc.gov.in", aadhaarNo = "8012-3456-7895"),
                    MemberEntity(orgId = mcId, memberCode = "MC-MEM-06", name = "Deepak Chauhan", role = "MEMBER", natureOfWork = "Urban Town Planning Officer", mobile = "9830022337", email = "planning.chauhan@mc.gov.in", aadhaarNo = "8012-3456-7896"),
                    MemberEntity(orgId = mcId, memberCode = "MC-MEM-07", name = "Fatima Sheikh", role = "MEMBER", natureOfWork = "Public Health and Hospital In-charge", mobile = "9830022338", email = "health.sheikh@mc.gov.in", aadhaarNo = "8012-3456-7897"),
                    MemberEntity(orgId = mcId, memberCode = "MC-MEM-08", name = "Santosh Yadav", role = "MEMBER", natureOfWork = "Hydraulic and Water Distribution Inspector", mobile = "9830022339", email = "water.yadav@mc.gov.in", aadhaarNo = "8012-3456-7898"),
                    MemberEntity(orgId = mcId, memberCode = "MC-MEM-09", name = "Rina Mukherjee", role = "MEMBER", natureOfWork = "Disaster Management and Fire Officer", mobile = "9830022340", email = "disaster.rina@mc.gov.in", aadhaarNo = "8012-3456-7899"),
                    MemberEntity(orgId = mcId, memberCode = "MC-MEM-10", name = "Ravi Teja", role = "MEMBER", natureOfWork = "Ward Field Verification Assistant", mobile = "9830022341", email = "field.teja@mc.gov.in", aadhaarNo = "8012-3456-7800")
                )
            )

            // Topic for Municipal Corporation
            database.votingTopicDao().insert(
                VotingTopicEntity(
                    orgId = mcId,
                    title = "Nigam Parishad General Ward Council Election",
                    description = "Cast your vote for Nigam Parishad representative to oversee municipal budget, drainage infrastructure, and citizen amenities.",
                    category = "Nigam Parishad Election",
                    optionsJson = "[\"Sunil Ghadge (Clean City Alliance)\", \"Anita Sawant (Civic Progress Front)\", \"Manoj Kadam (Independent Ward Forum)\"]",
                    createdAt = todayDate
                )
            )

            // 3. State/UT
            val stateId = database.organizationDao().insert(
                OrganizationEntity(
                    name = "State / UT Panchayati Raj Council",
                    code = "STATE_UT",
                    category = "State/UT",
                    purpose = "Caste vote for Panchayat Elections at panchayat level",
                    iconType = "panchayat",
                    morningShiftStart = "08:00",
                    morningShiftEnd = "12:00",
                    eveningShiftStart = "16:00",
                    eveningShiftEnd = "18:30"
                )
            )

            // 1 Admin + 10 Members for State/UT
            database.memberDao().insertAll(
                listOf(
                    MemberEntity(orgId = stateId, memberCode = "PR-ADM-01", name = "Dr. Alok Verma IAS", role = "ADMIN", natureOfWork = "District Collector and District Election Officer", mobile = "9840033441", email = "collector@statepr.gov.in", aadhaarNo = "7012-3456-7890"),
                    MemberEntity(orgId = stateId, memberCode = "PR-MEM-01", name = "Ramcharan Patil", role = "MEMBER", natureOfWork = "Gram Panchayat Head (Sarpanch Candidate)", mobile = "9840033442", email = "sarpanch.patil@statepr.gov.in", aadhaarNo = "7012-3456-7891"),
                    MemberEntity(orgId = stateId, memberCode = "PR-MEM-02", name = "Savitri Devi", role = "MEMBER", natureOfWork = "Panchayat Ward Member (Up-Sarpanch Candidate)", mobile = "9840033443", email = "savitri.devi@statepr.gov.in", aadhaarNo = "7012-3456-7892"),
                    MemberEntity(orgId = stateId, memberCode = "PR-MEM-03", name = "Dineshwar Tyagi", role = "MEMBER", natureOfWork = "Village Development Officer (VDO)", mobile = "9840033444", email = "vdo.tyagi@statepr.gov.in", aadhaarNo = "7012-3456-7893"),
                    MemberEntity(orgId = stateId, memberCode = "PR-MEM-04", name = "Bhimrao Kamble", role = "MEMBER", natureOfWork = "Panchayat Executive Secretary", mobile = "9840033445", email = "sec.kamble@statepr.gov.in", aadhaarNo = "7012-3456-7894"),
                    MemberEntity(orgId = stateId, memberCode = "PR-MEM-05", name = "Manju Lata", role = "MEMBER", natureOfWork = "Rural Women Self-Help Group Convener", mobile = "9840033446", email = "shg.manju@statepr.gov.in", aadhaarNo = "7012-3456-7895"),
                    MemberEntity(orgId = stateId, memberCode = "PR-MEM-06", name = "Kalyan Singh", role = "MEMBER", natureOfWork = "Rural Employment Guarantee Officer (MGNREGA)", mobile = "9840033447", email = "mgnrega.kalyan@statepr.gov.in", aadhaarNo = "7012-3456-7896"),
                    MemberEntity(orgId = stateId, memberCode = "PR-MEM-07", name = "Prem Chand", role = "MEMBER", natureOfWork = "Agriculture and Irrigation Field Officer", mobile = "9840033448", email = "agri.prem@statepr.gov.in", aadhaarNo = "7012-3456-7897"),
                    MemberEntity(orgId = stateId, memberCode = "PR-MEM-08", name = "Rekha Parmar", role = "MEMBER", natureOfWork = "Primary Health Centre (PHC) Worker", mobile = "9840033449", email = "phc.rekha@statepr.gov.in", aadhaarNo = "7012-3456-7898"),
                    MemberEntity(orgId = stateId, memberCode = "PR-MEM-09", name = "Mukesh Rawat", role = "MEMBER", natureOfWork = "Gram Panchayat Technical Assistant", mobile = "9840033450", email = "tech.mukesh@statepr.gov.in", aadhaarNo = "7012-3456-7899"),
                    MemberEntity(orgId = stateId, memberCode = "PR-MEM-10", name = "Gopal Krishna", role = "MEMBER", natureOfWork = "Drinking Water and Sanitation Sahayak", mobile = "9840033451", email = "water.gopal@statepr.gov.in", aadhaarNo = "7012-3456-7800")
                )
            )

            // Topic for State/UT
            database.votingTopicDao().insert(
                VotingTopicEntity(
                    orgId = stateId,
                    title = "Panchayat Elections at Panchayat Level: Sarpanch and Ward Council",
                    description = "Cast your vote for Gram Panchayat governance, rural road development, and primary health infrastructure fund management.",
                    category = "Panchayat Level Election",
                    optionsJson = "[\"Ramcharan Patil (Gram Pragati Panel)\", \"Savitri Devi (Kisan Vikas Samiti)\", \"Balram Choudhary (Independent)\"]",
                    createdAt = todayDate
                )
            )

            // 4. Housing Society
            val hsId = database.organizationDao().insert(
                OrganizationEntity(
                    name = "Emerald Heights Co-operative Housing Society",
                    code = "HOUSING_SOC",
                    category = "Housing Society",
                    purpose = "Caste vote for president, secretary, treasure etc",
                    iconType = "housing",
                    morningShiftStart = "08:00",
                    morningShiftEnd = "12:00",
                    eveningShiftStart = "17:00",
                    eveningShiftEnd = "20:00"
                )
            )

            // 1 Admin + 10 Members for Housing Society
            database.memberDao().insertAll(
                listOf(
                    MemberEntity(orgId = hsId, memberCode = "HS-ADM-01", name = "Col. Sanjeev Kapoor (Retd)", role = "ADMIN", natureOfWork = "Society Election Returning Officer and Chief Observer", mobile = "9850044551", email = "election.ro@emeraldheights.org", aadhaarNo = "6012-3456-7890"),
                    MemberEntity(orgId = hsId, memberCode = "HS-MEM-01", name = "Dr. Ashish Mehta", role = "MEMBER", natureOfWork = "Society President Candidate (Flat A-701)", mobile = "9850044552", email = "ashish.mehta@emeraldheights.org", aadhaarNo = "6012-3456-7891"),
                    MemberEntity(orgId = hsId, memberCode = "HS-MEM-02", name = "Smt. Shailaja Iyer", role = "MEMBER", natureOfWork = "Society General Secretary Candidate (Flat B-402)", mobile = "9850044553", email = "shailaja.iyer@emeraldheights.org", aadhaarNo = "6012-3456-7892"),
                    MemberEntity(orgId = hsId, memberCode = "HS-MEM-03", name = "Mr. Jayant Parekh", role = "MEMBER", natureOfWork = "Society Treasurer Candidate (Flat C-203)", mobile = "9850044554", email = "jayant.parekh@emeraldheights.org", aadhaarNo = "6012-3456-7893"),
                    MemberEntity(orgId = hsId, memberCode = "HS-MEM-04", name = "Capt. Rahul Mathur", role = "MEMBER", natureOfWork = "Security and Surveillance Committee Lead", mobile = "9850044555", email = "security@emeraldheights.org", aadhaarNo = "6012-3456-7894"),
                    MemberEntity(orgId = hsId, memberCode = "HS-MEM-05", name = "Vandana Rastogi", role = "MEMBER", natureOfWork = "Wing A Resident Delegate", mobile = "9850044556", email = "wing.a@emeraldheights.org", aadhaarNo = "6012-3456-7895"),
                    MemberEntity(orgId = hsId, memberCode = "HS-MEM-06", name = "Nitin Kulkarni", role = "MEMBER", natureOfWork = "Wing B Resident Delegate", mobile = "9850044557", email = "wing.b@emeraldheights.org", aadhaarNo = "6012-3456-7896"),
                    MemberEntity(orgId = hsId, memberCode = "HS-MEM-07", name = "Rohit Bansal", role = "MEMBER", natureOfWork = "Financial Audit and Accounts Inspector", mobile = "9850044558", email = "audit@emeraldheights.org", aadhaarNo = "6012-3456-7897"),
                    MemberEntity(orgId = hsId, memberCode = "HS-MEM-08", name = "Meera Subramanian", role = "MEMBER", natureOfWork = "Wing C Resident Delegate", mobile = "9850044559", email = "wing.c@emeraldheights.org", aadhaarNo = "6012-3456-7898"),
                    MemberEntity(orgId = hsId, memberCode = "HS-MEM-09", name = "Virendra Ahuja", role = "MEMBER", natureOfWork = "Facilities and Green Solar In-charge", mobile = "9850044560", email = "facilities@emeraldheights.org", aadhaarNo = "6012-3456-7899"),
                    MemberEntity(orgId = hsId, memberCode = "HS-MEM-10", name = "Sneha Sen", role = "MEMBER", natureOfWork = "Cultural and Community Welfare Secretary", mobile = "9850044561", email = "welfare@emeraldheights.org", aadhaarNo = "6012-3456-7800")
                )
            )

            // Topic for Housing Society
            database.votingTopicDao().insert(
                VotingTopicEntity(
                    orgId = hsId,
                    title = "Managing Committee Triennial Election: President, Secretary and Treasurer",
                    description = "Vote to elect the executive office bearers for Emerald Heights Housing Society. The elected team will supervise society maintenance, solar installation, and security contracts.",
                    category = "Office Bearers Election Announcement",
                    optionsJson = "[\"Panel 1: Dr. Ashish Mehta (President) and Smt. Shailaja Iyer (Secretary)\", \"Panel 2: Mr. Jayant Parekh (President) and Capt. Rahul Mathur (Secretary)\", \"Independent Candidates Slate\"]",
                    createdAt = todayDate
                )
            )

            // 5. Institute Committee
            val icId = database.organizationDao().insert(
                OrganizationEntity(
                    name = "Apex National Institute Academic Council",
                    code = "INSTITUTE",
                    category = "Institute Committee",
                    purpose = "Cast vote for president, etc",
                    iconType = "institute",
                    morningShiftStart = "09:00",
                    morningShiftEnd = "13:00",
                    eveningShiftStart = "14:00",
                    eveningShiftEnd = "17:30"
                )
            )

            // 1 Admin + 10 Members for Institute Committee
            database.memberDao().insertAll(
                listOf(
                    MemberEntity(orgId = icId, memberCode = "IC-ADM-01", name = "Prof. Narendra Bhargava", role = "ADMIN", natureOfWork = "Dean of Faculty and Committee Convener", mobile = "9860055661", email = "dean@institute.ac.in", aadhaarNo = "5012-3456-7890"),
                    MemberEntity(orgId = icId, memberCode = "IC-MEM-01", name = "Prof. Ananya Sen", role = "MEMBER", natureOfWork = "Faculty President Nominee (Dept of Computing)", mobile = "9860055662", email = "ananya.sen@institute.ac.in", aadhaarNo = "5012-3456-7891"),
                    MemberEntity(orgId = icId, memberCode = "IC-MEM-02", name = "Dr. Arvind Swaminathan", role = "MEMBER", natureOfWork = "Vice-President Nominee (Dept of Electronics)", mobile = "9860055663", email = "arvind.s@institute.ac.in", aadhaarNo = "5012-3456-7892"),
                    MemberEntity(orgId = icId, memberCode = "IC-MEM-03", name = "Prof. H. S. Chahal", role = "MEMBER", natureOfWork = "Academic Senate Secretary", mobile = "9860055664", email = "chahal@institute.ac.in", aadhaarNo = "5012-3456-7893"),
                    MemberEntity(orgId = icId, memberCode = "IC-MEM-04", name = "Dr. Pallavi Joshi", role = "MEMBER", natureOfWork = "Research and Grants Council Chair", mobile = "9860055665", email = "pallavi.j@institute.ac.in", aadhaarNo = "5012-3456-7894"),
                    MemberEntity(orgId = icId, memberCode = "IC-MEM-05", name = "Prof. T. K. Roy", role = "MEMBER", natureOfWork = "Curriculum and Syllabus Delegate", mobile = "9860055666", email = "roy.tk@institute.ac.in", aadhaarNo = "5012-3456-7895"),
                    MemberEntity(orgId = icId, memberCode = "IC-MEM-06", name = "Dr. Monica Sharma", role = "MEMBER", natureOfWork = "Advanced Laboratories Director", mobile = "9860055667", email = "monica.sharma@institute.ac.in", aadhaarNo = "5012-3456-7896"),
                    MemberEntity(orgId = icId, memberCode = "IC-MEM-07", name = "Sanjay Singhania", role = "MEMBER", natureOfWork = "Central Library and Digital Resources Head", mobile = "9860055668", email = "library@institute.ac.in", aadhaarNo = "5012-3456-7897"),
                    MemberEntity(orgId = icId, memberCode = "IC-MEM-08", name = "Dr. Rakesh Tiwari", role = "MEMBER", natureOfWork = "Dean of Student Affairs and Welfare", mobile = "9860055669", email = "studentaffairs@institute.ac.in", aadhaarNo = "5012-3456-7898"),
                    MemberEntity(orgId = icId, memberCode = "IC-MEM-09", name = "Smita Kulkarni", role = "MEMBER", natureOfWork = "Doctoral Researchers Representative", mobile = "9860055670", email = "phd.rep@institute.ac.in", aadhaarNo = "5012-3456-7899"),
                    MemberEntity(orgId = icId, memberCode = "IC-MEM-10", name = "Amitabh Ghosh", role = "MEMBER", natureOfWork = "Chief Technical Officer and Registrar Liaison", mobile = "9860055671", email = "cto@institute.ac.in", aadhaarNo = "5012-3456-7800")
                )
            )

            // Topic for Institute Committee
            database.votingTopicDao().insert(
                VotingTopicEntity(
                    orgId = icId,
                    title = "Institute Governing Council: Election of President and Executive Board",
                    description = "Cast your vote for Institute Committee President. The elected president will steer AI research funding, laboratory modernizations, and faculty tenure policies.",
                    category = "Executive Committee Election",
                    optionsJson = "[\"Prof. Ananya Sen (Progressive Research Coalition)\", \"Dr. Arvind Swaminathan (Faculty Alliance Panel)\", \"Prof. H. S. Chahal (Academic Excellence Guild)\"]",
                    createdAt = todayDate
                )
            )

            // 6. Election Authority
            val eaId = database.organizationDao().insert(
                OrganizationEntity(
                    name = "Apex Democratic Election Commission",
                    code = "ELECTION_AUTH",
                    category = "Election Authority",
                    purpose = "cast vote for good governance",
                    iconType = "governance",
                    morningShiftStart = "08:30",
                    morningShiftEnd = "12:30",
                    eveningShiftStart = "15:30",
                    eveningShiftEnd = "18:30"
                )
            )

            // 1 Admin + 10 Members for Election Authority
            database.memberDao().insertAll(
                listOf(
                    MemberEntity(orgId = eaId, memberCode = "EA-ADM-01", name = "Dr. S. K. Krishnamurthy", role = "ADMIN", natureOfWork = "Chief Election Commissioner and Governance Overseer", mobile = "9870066771", email = "cec@electionauth.gov.in", aadhaarNo = "4012-3456-7890"),
                    MemberEntity(orgId = eaId, memberCode = "EA-MEM-01", name = "Sudhir Malhotra", role = "MEMBER", natureOfWork = "Good Governance and Public Integrity Auditor", mobile = "9870066772", email = "governance.sudhir@electionauth.gov.in", aadhaarNo = "4012-3456-7891"),
                    MemberEntity(orgId = eaId, memberCode = "EA-MEM-02", name = "Neeta Saxena", role = "MEMBER", natureOfWork = "Public Policy and Transparency Scrutineer", mobile = "9870066773", email = "transparency.neeta@electionauth.gov.in", aadhaarNo = "4012-3456-7892"),
                    MemberEntity(orgId = eaId, memberCode = "EA-MEM-03", name = "Ranjan Sen", role = "MEMBER", natureOfWork = "Vigilance and Anti-Corruption Officer", mobile = "9870066774", email = "vigilance.ranjan@electionauth.gov.in", aadhaarNo = "4012-3456-7893"),
                    MemberEntity(orgId = eaId, memberCode = "EA-MEM-04", name = "Gauri Pathak", role = "MEMBER", natureOfWork = "Democratic Outreach and Civic Participation Lead", mobile = "9870066775", email = "civic.gauri@electionauth.gov.in", aadhaarNo = "4012-3456-7894"),
                    MemberEntity(orgId = eaId, memberCode = "EA-MEM-05", name = "Hemant Bisht", role = "MEMBER", natureOfWork = "Electoral Roll and Identity Verification Officer", mobile = "9870066776", email = "electoral.hemant@electionauth.gov.in", aadhaarNo = "4012-3456-7895"),
                    MemberEntity(orgId = eaId, memberCode = "EA-MEM-06", name = "Divya Balan", role = "MEMBER", natureOfWork = "Legal Compliance and Code of Conduct Inspector", mobile = "9870066777", email = "compliance.divya@electionauth.gov.in", aadhaarNo = "4012-3456-7896"),
                    MemberEntity(orgId = eaId, memberCode = "EA-MEM-07", name = "Tanmoy Sarkar", role = "MEMBER", natureOfWork = "Digital Voting Security and Cyber Assurance Lead", mobile = "9870066778", email = "cyber.tanmoy@electionauth.gov.in", aadhaarNo = "4012-3456-7897"),
                    MemberEntity(orgId = eaId, memberCode = "EA-MEM-08", name = "Pooja Hegde", role = "MEMBER", natureOfWork = "Citizen Grievance and Redressal Officer", mobile = "9870066779", email = "grievance.pooja@electionauth.gov.in", aadhaarNo = "4012-3456-7898"),
                    MemberEntity(orgId = eaId, memberCode = "EA-MEM-09", name = "Vikas Aggarwal", role = "MEMBER", natureOfWork = "Independent Election Observer Liaison", mobile = "9870066780", email = "observer.vikas@electionauth.gov.in", aadhaarNo = "4012-3456-7899"),
                    MemberEntity(orgId = eaId, memberCode = "EA-MEM-10", name = "Suraj Prakash", role = "MEMBER", natureOfWork = "Polling Logistics and Materials In-charge", mobile = "9870066781", email = "logistics.suraj@electionauth.gov.in", aadhaarNo = "4012-3456-7800")
                )
            )

            // Topic for Election Authority
            database.votingTopicDao().insert(
                VotingTopicEntity(
                    orgId = eaId,
                    title = "Good Governance Citizens Charter and Transparency Reform 2026",
                    description = "Vote on key good governance proposals: Mandatory digital grievance redressal within 48 hours, algorithmic transparency, and decentralized civic audits.",
                    category = "Good Governance Referendum",
                    optionsJson = "[\"Resolution A: Adopt Digital Fast-Track Grievance and Full Public Audit\", \"Resolution B: Phase-Wise Municipal Redressal with Local Committee Oversight\", \"Resolution C: Retain Current Framework with Annual Review\"]",
                    createdAt = todayDate
                )
            )
        }
    }
}
