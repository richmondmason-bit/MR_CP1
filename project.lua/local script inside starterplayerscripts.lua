--This is the sliding mechanic in fathom
--all scripts go inside of ServerscriptScripts
--make a dummy and all enemies named "zombie" with a humanoid+ humanoidrootpart for damage and hitboxes



-- Services
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local Debris = game:GetService("Debris")

-- RemoteEvents
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

-- Constants
local MAX_STAMINA = 100
local STAMINA_REGEN_RATE = 10 -- per second

local DASH_STAMINA_COST = 20
local DASH_COOLDOWN = 1 -- seconds

local SLIDE_STAMINA_COST = 15
local SLIDE_COOLDOWN = 2

local VAULT_STAMINA_COST = 10
local VAULT_COOLDOWN = 1.5

local DROP_KICK_STAMINA_COST = 25
local DROP_KICK_COOLDOWN = 3

local MELEE_COOLDOWN = 0.7 -- Melee has no stamina cost, but has cooldown

local DASH_DISTANCE = 50
local DASH_DURATION = 0.2

local SLIDE_SPEED = 50
local SLIDE_DURATION = 1

local VAULT_MAX_HEIGHT = 5
local VAULT_DURATION = 0.7

local DROP_KICK_DAMAGE = 50
local SLIDE_DAMAGE = 10
local MELEE_DAMAGE = 10

-- Tables to track player states
local playerStates = {}

-- Helper: Initialize player data
local function initPlayerData(player)
	playerStates[player] = {
		Stamina = MAX_STAMINA,
		Cooldowns = {
			Dash = false,
			Slide = false,
			Vault = false,
			Dropkick = false,
			Melee = false,
		},
		Sliding = false,
		Vaulting = false,
		OriginalWalkSpeed = 16,
	}
end

local function cleanupPlayerData(player)
	playerStates[player] = nil
end

-- Helper: Check if a model is a zombie
local function isZombie(model)
	return model:IsA("Model") and
	       model:FindFirstChild("Humanoid") and
	       model:FindFirstChild("HumanoidRootPart") and
	       model.Name == "Zombie"
end

-- Helper: Get character components safely
local function getCharacterComponents(player)
	local character = player.Character
	if not character then return end
	local humanoid = character:FindFirstChild("Humanoid")
	local rootPart = character:FindFirstChild("HumanoidRootPart")
	if not humanoid or not rootPart then return end
	return character, humanoid, rootPart
end

-- Helper: Apply cooldown and notify client
local function applyCooldown(player, actionName, cooldownTime)
	local state = playerStates[player]
	if not state then return end
	state.Cooldowns[actionName] = true

	-- Fire cooldown UI update to client
	if actionName == "Dash" then
		DashCooldownEvent:FireClient(player, cooldownTime)
	elseif actionName == "Slide" then
		SlideCooldownEvent:FireClient(player, cooldownTime)
	elseif actionName == "Vault" then
		VaultCooldownEvent:FireClient(player, cooldownTime)
	elseif actionName == "Dropkick" then
		DropkickCooldownEvent:FireClient(player, cooldownTime)
	end

	-- After cooldown, reset flag
	task.delay(cooldownTime, function()
		if playerStates[player] then
			playerStates[player].Cooldowns[actionName] = false
		end
	end)
end

-- Stamina updater for players (regen stamina periodically)
RunService.Heartbeat:Connect(function(dt)
	for player, state in pairs(playerStates) do
		if state then
			-- Regenerate stamina only if player is not actively using stamina abilities
			if not (state.Cooldowns.Dash or state.Cooldowns.Slide or state.Cooldowns.Vault or state.Cooldowns.Dropkick) then
				state.Stamina = math.min(MAX_STAMINA, state.Stamina + STAMINA_REGEN_RATE * dt)
				StaminaUpdateEvent:FireClient(player, state.Stamina, MAX_STAMINA)
			end
		end
	end
end)

-- Handle Dash
DashEvent.OnServerEvent:Connect(function(player)
	local state = playerStates[player]
	if not state then return end

	if state.Cooldowns.Dash or state.Stamina < DASH_STAMINA_COST or state.Sliding or state.Vaulting then
		return -- reject request
	end

	local character, humanoid, rootPart = getCharacterComponents(player)
	if not character then return end

	state.Stamina = state.Stamina - DASH_STAMINA_COST
	applyCooldown(player, "Dash", DASH_COOLDOWN)
	StaminaUpdateEvent:FireClient(player, state.Stamina, MAX_STAMINA)

	-- Perform Dash movement using BodyVelocity for smoother physics
	local direction = rootPart.CFrame.LookVector
	local bv = Instance.new("BodyVelocity")
	bv.Velocity = direction * (DASH_DISTANCE / DASH_DURATION)
	bv.MaxForce = Vector3.new(1e5, 1e5, 1e5)
	bv.P = 12500
	bv.Parent = rootPart

	Debris:AddItem(bv, DASH_DURATION)
end)

-- Handle Slide
SlideEvent.OnServerEvent:Connect(function(player)
	local state = playerStates[player]
	if not state then return end

	if state.Cooldowns.Slide or state.Stamina < SLIDE_STAMINA_COST or state.Sliding or state.Vaulting then
		return -- reject
	end

	local character, humanoid, rootPart = getCharacterComponents(player)
	if not character then return end

	state.Stamina = state.Stamina - SLIDE_STAMINA_COST
	state.Sliding = true
	applyCooldown(player, "Slide", SLIDE_COOLDOWN)
	StaminaUpdateEvent:FireClient(player, state.Stamina, MAX_STAMINA)

	-- Store original walk speed to reset later
	state.OriginalWalkSpeed = humanoid.WalkSpeed
	humanoid.WalkSpeed = 0

	local slideStart = tick()
	local direction = rootPart.CFrame.LookVector
	local slideHitCooldown = {}

	-- Slide mechanic loop in coroutine
	coroutine.wrap(function()
		while tick() - slideStart < SLIDE_DURATION do
			rootPart.Velocity = direction * SLIDE_SPEED

			-- Damage zombies in range
			for _, obj in ipairs(workspace:GetChildren()) do
				if isZombie(obj) and not slideHitCooldown[obj] then
					local dist = (obj.HumanoidRootPart.Position - rootPart.Position).Magnitude
					if dist < 4 then
						local bv = Instance.new("BodyVelocity")
						bv.Velocity = direction * 60 + Vector3.new(0, 30, 0)
						bv.MaxForce = Vector3.new(1e5, 1e5, 1e5)
						bv.P = 12500
						bv.Parent = obj.HumanoidRootPart
						Debris:AddItem(bv, 0.3)

						obj.Humanoid:TakeDamage(SLIDE_DAMAGE)
						slideHitCooldown[obj] = true
					end
				end
			end

			RunService.Heartbeat:Wait()
		end

		-- Reset slide state and walk speed safely
		state.Sliding = false
		if humanoid and humanoid.Parent then
			humanoid.WalkSpeed = state.OriginalWalkSpeed or 16
		end
	end)()
end)

-- Handle Vault
VaultEvent.OnServerEvent:Connect(function(player)
	local state = playerStates[player]
	if not state then return end

	if state.Cooldowns.Vault or state.Stamina < VAULT_STAMINA_COST or state.Sliding or state.Vaulting then
		return -- reject
	end

	local character, humanoid, rootPart = getCharacterComponents(player)
	if not character then return end

	state.Stamina = state.Stamina - VAULT_STAMINA_COST
	state.Vaulting = true
	applyCooldown(player, "Vault", VAULT_COOLDOWN)
	StaminaUpdateEvent:FireClient(player, state.Stamina, MAX_STAMINA)

	-- Vault mechanic: raycast forward to find obstacle
	local direction = rootPart.CFrame.LookVector * 5
	local rayParams = RaycastParams.new()
	rayParams.FilterDescendantsInstances = {character}
	rayParams.FilterType = Enum.RaycastFilterType.Blacklist
	local result = workspace:Raycast(rootPart.Position, direction, rayParams)

	if result then
		local part = result.Instance
		if part and part.Parent then
			local topY = part.Position.Y + part.Size.Y / 2
			local feetY = rootPart.Position.Y - character:GetExtentsSize().Y / 2
			local height = topY - feetY

			if height <= VAULT_MAX_HEIGHT then
				local vaultOffset = Vector3.new(direction.X, height + 2, direction.Z)
				local targetPosition = rootPart.Position + vaultOffset
				local startTime = tick()
				local startPos = rootPart.Position

				while tick() - startTime < VAULT_DURATION do
					local alpha = (tick() - startTime) / VAULT_DURATION
					local pos = startPos:Lerp(targetPosition, alpha)
					rootPart.CFrame = CFrame.new(pos, pos + rootPart.CFrame.LookVector)
					RunService.Heartbeat:Wait()
				end

				rootPart.CFrame = CFrame.new(targetPosition, targetPosition + rootPart.CFrame.LookVector)
			end
		end
	end

	state.Vaulting = false
end)

-- Handle Dropkick
DropkickEvent.OnServerEvent:Connect(function(player)
	local state = playerStates[player]
	if not state then return end

	if state.Cooldowns.Dropkick or state.Stamina < DROP_KICK_STAMINA_COST or state.Sliding or state.Vaulting then
		return -- reject
	end

	local character, humanoid, rootPart = getCharacterComponents(player)
	if not character then return end

	state.Stamina = state.Stamina - DROP_KICK_STAMINA_COST
	applyCooldown(player, "Dropkick", DROP_KICK_COOLDOWN)
	StaminaUpdateEvent:FireClient(player, state.Stamina, MAX_STAMINA)

	local direction = rootPart.CFrame.LookVector

	-- Knockback player using BodyVelocity
	local bv = Instance.new("BodyVelocity")
	bv.Velocity = direction * 50 + Vector3.new(0, 20, 0)
	bv.MaxForce = Vector3.new(1e5, 1e5, 1e5)
	bv.P = 12500
	bv.Parent = rootPart
	Debris:AddItem(bv, 0.3)

	-- Damage zombies in front with angle check
	for _, obj in ipairs(workspace:GetChildren()) do
		if isZombie(obj) and obj:FindFirstChild("HumanoidRootPart") then
			local toZombie = obj.HumanoidRootPart.Position - rootPart.Position
			local dist = toZombie.Magnitude
			if dist < 6 then
				local angle = math.acos(toZombie.Unit:Dot(direction))
				if angle < math.rad(45) then
					obj.Humanoid:TakeDamage(DROP_KICK_DAMAGE)

					-- Knockback zombie
					local knockback = Instance.new("BodyVelocity")
					knockback.Velocity = direction * 40 + Vector3.new(0, 15, 0)
					knockback.MaxForce = Vector3.new(1e5, 1e5, 1e5)
					knockback.P = 12500
					knockback.Parent = obj.HumanoidRootPart
					Debris:AddItem(knockback, 0.3)
				end
			end
		end
	end
end)

-- Handle Melee
MeleeEvent.OnServerEvent:Connect(function(player)
	local state = playerStates[player]
	if not state then return end

	if state.Cooldowns.Melee then return end

	local character, humanoid, rootPart = getCharacterComponents(player)
	if not character then return end

	applyCooldown(player, "Melee", MELEE_COOLDOWN)

	local direction = rootPart.CFrame.LookVector
	for _, obj in ipairs(workspace:GetChildren()) do
		if isZombie(obj) and obj:FindFirstChild("HumanoidRootPart") then
			local toZombie = obj.HumanoidRootPart.Position - rootPart.Position
			local dist = toZombie.Magnitude
			if dist < 5 then
				local angle = math.acos(toZombie.Unit:Dot(direction))
				if angle < math.rad(60) then
					obj.Humanoid:TakeDamage(MELEE_DAMAGE)
				end
			end
		end
	end
end)

-- Player join/leave management
Players.PlayerAdded:Connect(function(player)
	initPlayerData(player)
end)

Players.PlayerRemoving:Connect(function(player)
	cleanupPlayerData(player)
end)

-- Initialize for existing players
for _, player in pairs(Players:GetPlayers()) do
	initPlayerData(player)
end
