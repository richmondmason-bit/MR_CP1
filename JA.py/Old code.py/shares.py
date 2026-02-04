# MR, Period 1, Crew Shares Assignment

# Input total amount earned and number of crew members
total_earned = float(input("How much was earned: "))
crew_count = int(input("How many crew members are there (not including the captain and first mate): "))

total_shares = 7 + 3 + crew_count


share_value = total_earned / total_shares

captain_gets = 7 * share_value
first_mate_gets = 3 * share_value
crew_full_share = share_value

crew_still_needs = crew_full_share - 500


captain_gets = round(captain_gets, 2)
first_mate_gets = round(first_mate_gets, 2)
crew_still_needs = round(crew_still_needs, 2)

# Output
print("\n--- Payment Majiggie ---")
print(f"The captain gets: ${captain_gets:,.2f}")
print(f"The first mate gets: ${first_mate_gets:,.2f}")
print(f"Crew still needs: ${crew_still_needs:,.2f} each")

hello = 1