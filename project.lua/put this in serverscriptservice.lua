local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local Debris = game:GetService("Debris")

-- Events
local DashEvent = ReplicatedStorage:WaitForChild("DashEvent")
local SlideEvent = ReplicatedStorage:WaitForChild("SlideEvent")
local VaultEvent = ReplicatedStorage:WaitForChild("VaultEvent")
local MeleeEvent = ReplicatedStorage:WaitForChild("MeleeEvent")
local DropkickEvent = ReplicatedStorage:WaitForChild("DropkickEvent")

local DashCooldownEvent = ReplicatedStorage:WaitForChild("DashCooldownEvent")
local SlideCooldownEvent = ReplicatedStorage:WaitForChild("SlideCooldownEvent")
local VaultCooldownEvent = ReplicatedStorage:WaitForChild("VaultCooldownEvent")
local DropkickCooldownEvent = ReplicatedStorage:WaitForChild("DropkickCooldownEvent")
local StaminaUpdateEvent = ReplicatedStorage:WaitForChild("StaminaUpdateEvent")

-- Ability cooldowns and stamina costs (seconds & points)
local COOLDOWNS = {
	Dash = 1,
	Slide = 1,
	Vault = 1,
	Dropkick = 2,
}

local STAMINA_COST = {
	Dash = 20,
	Slide = 30,
	Vault = 15,
	Dropkick = 40,
}

local MAX_STAMINA = 100
local STAMINA_REGEN_RATE = 15 -- per second
local STAMINA_REGEN_DELAY = 3 -- seconds after depletion before regen starts

-- Track stamina and cooldowns per player
local playerData = {}

local function initPlayerData(player)
	playerData[player] = {
		stamina = MAX_STAMINA,
		cooldowns = {},
		lastStaminaUse = 0,
	}
end

local function cleanupPlayerData(player)
	playerData[player] = nil
end

Players.PlayerAdded:Connect(initPlayerData)
Players.PlayerRemoving:Connect(cleanupPlayerData)

-- Stamina regeneration loop
RunService.Heartbeat:Connect(function(dt)
	for player, data in pairs(playerData) do
		local now = tick()
		-- Only regen if cooldown passed since last stamina use
		if now - data.lastStaminaUse >= STAMINA_REGEN_DELAY then
			if data.stamina < MAX_STAMINA then
				data.stamina = math.min(MAX_STAMINA, data.stamina + STAMINA_REGEN_RATE * dt)
				StaminaUpdateEvent:FireClient(player, data.stamina, MAX_STAMINA)
			end
		end
	end
end)

-- Helper to check cooldown
local function canUse(player, ability)
	local now = tick()
	local data = playerData[player]
	if not data then return false end

	local cd = data.cooldowns[ability]
	if cd and cd > now then
		return false
	end

	-- Check stamina
	local cost = STAMINA_COST[ability] or 0
	if data.stamina < cost then
		return false
	end

	return true
end

-- Set cooldown and consume stamina
local function useAbility(player, ability)
	local data = playerData[player]
	if not data then return end

	local now = tick()
	data.cooldowns[ability] = now + (COOLDOWNS[ability] or 1)
	local cost = STAMINA_COST[ability] or 0
	data.stamina = math.max(0, data.stamina - cost)
	data.lastStaminaUse = now
	StaminaUpdateEvent:FireClient(player, data.stamina, MAX_STAMINA)
end

-- Helper to identify zombies
local function isZombie(model)
	return model:IsA("Model") and model:FindFirstChild("Humanoid") and model:FindFirstChild("HumanoidRootPart") and model.Name == "Zombie"
end

-- Ability implementations (server side effects)

-- For simplicity, only dropkick and slide affect zombies here
local function doSlide(player)
	local character = player.Character
	if not character then return end
	local rootPart = character:FindFirstChild("HumanoidRootPart")
	if not rootPart then return end

	local direction = rootPart.CFrame.LookVector

	-- Push zombies near the player during slide
	for _, obj in ipairs(workspace:GetChildren()) do
		if isZombie(obj) then
			local dist = (obj.HumanoidRootPart.Position - rootPart.Position).Magnitude
			if dist < 4 then
				local bv = Instance.new("BodyVelocity")
				bv.Velocity = direction * 60 + Vector3.new(0, 30, 0)
				bv.MaxForce = Vector3.new(1e5, 1e5, 1e5)
				bv.P = 12500
				bv.Parent = obj.HumanoidRootPart
				Debris:AddItem(bv, 0.3)

				obj.Humanoid:TakeDamage(10)
			end
		end
	end
end

local function doDropkick(player)
	local character = player.Character
	if not character then return end
	local rootPart = character:FindFirstChild("HumanoidRootPart")
	if not rootPart then return end
	local direction = rootPart.CFrame.LookVector

	for _, obj in ipairs(workspace:GetChildren()) do
		if isZombie(obj) then
			local dist = (obj.HumanoidRootPart.Position - rootPart.Position).Magnitude
			if dist < 6 then
				local bv = Instance.new("BodyVelocity")
				bv.Velocity = direction * 80 + Vector3.new(0, 50, 0)
				bv.MaxForce = Vector3.new(1e6, 1e6, 1e6)
				bv.P = 12500
				bv.Parent = obj.HumanoidRootPart
				Debris:AddItem(bv, 0.4)

				obj.Humanoid:TakeDamage(50)
			end
		end
	end
end

-- Listen to RemoteEvents for abilities

DashEvent.OnServerEvent:Connect(function(player)
	if not canUse(player, "Dash") then return end
	useAbility(player, "Dash")
	-- You can trigger server-side dash movement here or just notify client
	DashCooldownEvent:FireClient(player, COOLDOWNS.Dash)
	-- For example, you can implement dash velocity here if you want server authoritative movement
	print(player.Name .. " dashed")
end)

SlideEvent.OnServerEvent:Connect(function(player)
	if not canUse(player, "Slide") then return end
	useAbility(player, "Slide")
	SlideCooldownEvent:FireClient(player, COOLDOWNS.Slide)
	doSlide(player)
	print(player.Name .. " slid")
end)

VaultEvent.OnServerEvent:Connect(function(player)
	if not canUse(player, "Vault") then return end
	useAbility(player, "Vault")
	VaultCooldownEvent:FireClient(player, COOLDOWNS.Vault)
	-- Vault movement can be handled client-side for smoothness, but validated here
	print(player.Name .. " vaulted")
end)

DropkickEvent.OnServerEvent:Connect(function(player)
	if not canUse(player, "Dropkick") then return end
	useAbility(player, "Dropkick")
	DropkickCooldownEvent:FireClient(player, COOLDOWNS.Dropkick)
	doDropkick(player)
	print(player.Name .. " dropkicked")
end)

MeleeEvent.OnServerEvent:Connect(function(player)
	-- You can add stamina cost and cooldown if needed
	print(player.Name .. " melee attacked")
end)
