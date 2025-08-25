--This is the sliding mechanic in fathom
--all scripts go inside of StarterPlayerScripts
--make a dummy and all enemies named "zombie" with a humanoid+ humanoidrootpart for damage and hitboxes



-- LocalScript: PlayerMovementAndCombat (vault triggered by Space)

local Players = game:GetService("Players")
local UserInputService = game:GetService("UserInputService")
local RunService = game:GetService("RunService")
local Debris = game:GetService("Debris")

local player = Players.LocalPlayer
local character = player.Character or player.CharacterAdded:Wait()
local humanoid = character:WaitForChild("Humanoid")
local rootPart = character:WaitForChild("HumanoidRootPart")

-- Animation IDs (replace these with your uploaded animation asset IDs)
local SLIDE_ANIMATION_ID = "rbxassetid://YOUR_SLIDE_ANIMATION_ID"
local DROPKICK_ANIMATION_ID = "rbxassetid://YOUR_DROPKICK_ANIMATION_ID"
local MELEE_ANIMATION_ID = "rbxassetid://YOUR_MELEE_ANIMATION_ID"
local VAULT_ANIMATION_ID = "rbxassetid://YOUR_VAULT_ANIMATION_ID"

-- Movement speeds
local normalSpeed = 16
local sprintSpeed = 28
local slideSpeed = 50

-- States
local isSprinting = false
local sliding = false
local dropkickCooldown = false
local inAir = false
local vaulting = false

-- Track humanoid states for jump/fall detection
humanoid.StateChanged:Connect(function(_, newState)
	if newState == Enum.HumanoidStateType.Freefall then
		inAir = true
	elseif newState == Enum.HumanoidStateType.Landed or newState == Enum.HumanoidStateType.Running then
		inAir = false
	end
end)

-- Helper: Check if model is a zombie
local function isZombie(model)
	return model:IsA("Model")
		and model:FindFirstChild("Humanoid")
		and model:FindFirstChild("HumanoidRootPart")
		and model.Name == "Zombie"
end

-- Sprint input handlers
UserInputService.InputBegan:Connect(function(input, processed)
	if processed then return end

	if input.KeyCode == Enum.KeyCode.LeftShift then
		isSprinting = true
		if not sliding and not vaulting then
			humanoid.WalkSpeed = sprintSpeed
		end
	end
end)

UserInputService.InputEnded:Connect(function(input)
	if input.KeyCode == Enum.KeyCode.LeftShift then
		isSprinting = false
		if not sliding and not vaulting then
			humanoid.WalkSpeed = normalSpeed
		end
	end
end)

-- Slide function
local function slide()
	sliding = true

	-- Play slide animation
	local slideAnim = Instance.new("Animation")
	slideAnim.AnimationId = SLIDE_ANIMATION_ID
	local animTrack = humanoid:LoadAnimation(slideAnim)
	animTrack:Play()

	local direction = rootPart.CFrame.LookVector
	local slideDuration = 1
	local slideStartTime = tick()
	local slideHitCooldown = {}

	while tick() - slideStartTime < slideDuration do
		rootPart.Velocity = direction * slideSpeed

		-- Detect and fling zombies
		for _, obj in ipairs(workspace:GetChildren()) do
			if isZombie(obj) and not slideHitCooldown[obj] then
				local enemyRoot = obj.HumanoidRootPart
				local distance = (enemyRoot.Position - rootPart.Position).Magnitude

				if distance < 4 then
					local bodyVelocity = Instance.new("BodyVelocity")
					bodyVelocity.Velocity = direction * 60 + Vector3.new(0, 30, 0)
					bodyVelocity.MaxForce = Vector3.new(1e5, 1e5, 1e5)
					bodyVelocity.P = 12500
					bodyVelocity.Parent = enemyRoot

					Debris:AddItem(bodyVelocity, 0.3)

					obj.Humanoid:TakeDamage(10)

					slideHitCooldown[obj] = true
				end
			end
		end

		RunService.RenderStepped:Wait()
	end

	sliding = false

	-- Restore speed
	if isSprinting then
		humanoid.WalkSpeed = sprintSpeed
	else
		humanoid.WalkSpeed = normalSpeed
	end
end

-- Dropkick function
local function dropkick()
	dropkickCooldown = true

	local kickAnim = Instance.new("Animation")
	kickAnim.AnimationId = DROPKICK_ANIMATION_ID
	local track = humanoid:LoadAnimation(kickAnim)
	track:Play()

	local duration = 1
	local hitZombies = {}
	local startTime = tick()

	while tick() - startTime < duration do
		for _, obj in ipairs(workspace:GetChildren()) do
			if isZombie(obj) and not hitZombies[obj] then
				local dist = (obj.HumanoidRootPart.Position - rootPart.Position).Magnitude
				if dist < 6 then
					local bv = Instance.new("BodyVelocity")
					bv.Velocity = rootPart.CFrame.LookVector * 80 + Vector3.new(0, 50, 0)
					bv.MaxForce = Vector3.new(1e6, 1e6, 1e6)
					bv.P = 12500
					bv.Parent = obj.HumanoidRootPart
					Debris:AddItem(bv, 0.4)

					obj.Humanoid:TakeDamage(50)
					hitZombies[obj] = true
				end
			end
		end
		RunService.RenderStepped:Wait()
	end

	wait(2)
	dropkickCooldown = false
end

-- Regular melee function
local function melee()
	local anim = Instance.new("Animation")
	anim.AnimationId = MELEE_ANIMATION_ID
	local track = humanoid:LoadAnimation(anim)
	track:Play()

	local hitZombies = {}
	local startTime = tick()
	local duration = 0.7


	while tick() - startTime < duration do
		for _, obj in ipairs(workspace:GetChildren()) do
			if isZombie(obj) and not hitZombies[obj] then
				local dist = (obj.HumanoidRootPart.Position - rootPart.Position).Magnitude
				if dist < 5 then
					obj.Humanoid:TakeDamage(10)
					hitZombies[obj] = true
				end
			end
		end
		RunService.RenderStepped:Wait()
	end
end

-- Vault function
local function vault()
	if vaulting or sliding then return end  -- prevent overlap
	vaulting = true

	-- Cast ray forward to find vaultable obstacle
	local vaultRange = 5
	local vaultHeightLimit = 5

	local origin = rootPart.Position
	local direction = rootPart.CFrame.LookVector * vaultRange

	local raycastParams = RaycastParams.new()
	raycastParams.FilterDescendantsInstances = {character}
	raycastParams.FilterType = Enum.RaycastFilterType.Blacklist

	local raycastResult = workspace:Raycast(origin, direction, raycastParams)
	if raycastResult then
		local hitPart = raycastResult.Instance
		local hitPos = raycastResult.Position

		-- Check if obstacle height is vaultable
		local obstacleHeight = hitPart.Size.Y
		if obstacleHeight <= vaultHeightLimit then
			-- Play vault animation
			local vaultAnim = Instance.new("Animation")
			vaultAnim.AnimationId = VAULT_ANIMATION_ID
			local animTrack = humanoid:LoadAnimation(vaultAnim)
			animTrack:Play()

			-- Calculate vault destination (move player over obstacle)
			local vaultOffset = Vector3.new(direction.X, obstacleHeight + 2, direction.Z)
			local targetPosition = rootPart.Position + vaultOffset

			-- Smoothly move player over obstacle
			local duration = 0.7
			local startTime = tick()
			local startPos = rootPart.Position

			while tick() - startTime < duration do
				local alpha = (tick() - startTime) / duration
				local newPos = startPos:Lerp(targetPosition, alpha)
				rootPart.CFrame = CFrame.new(newPos.X, newPos.Y, newPos.Z) * CFrame.Angles(0, rootPart.Orientation.Y, 0)
				RunService.RenderStepped:Wait()
			end

			-- Ensure final position is set precisely
			rootPart.CFrame = CFrame.new(targetPosition.X, targetPosition.Y, targetPosition.Z) * CFrame.Angles(0, rootPart.Orientation.Y, 0)
		end
	end

	vaulting = false
end

-- Slide input handler
UserInputService.InputBegan:Connect(function(input, processed)
	if processed then return end

	if input.KeyCode == Enum.KeyCode.LeftControl and isSprinting and not sliding then
		slide()
	end
end)

-- Combat input handler (melee or dropkick)
UserInputService.InputBegan:Connect(function(input, processed)
	if processed then return end

	if input.KeyCode == Enum.KeyCode.V and not dropkickCooldown then
		if isSprinting and inAir then
			dropkick()
		else
			melee()
		end
	end
end)

-- Vault input handler (press Spacebar)
UserInputService.InputBegan:Connect(function(input, processed)
	if processed then return end

	if input.KeyCode == Enum.KeyCode.Space then
		vault()
	end
end)


-- Dash settings
local dashDistance = 50
local dashDuration = 0.2
local dashCooldownTime = 1
local dashStaminaCost = 20
local canDash = true

local function dash()
	if not canDash or stamina < dashStaminaCost or sliding or vaulting or staminaCooldown then
		return
	end

	canDash = false
	stamina = stamina - dashStaminaCost

	local dashStart = tick()
	local dashDirection = rootPart.CFrame.LookVector
	local startPos = rootPart.Position

	-- Disable humanoid controls briefly for dash
	humanoid.WalkSpeed = 0

	while tick() - dashStart < dashDuration do
		local alpha = (tick() - dashStart) / dashDuration
		local newPos = startPos + dashDirection * dashDistance * alpha
		rootPart.CFrame = CFrame.new(newPos.X, newPos.Y, newPos.Z, rootPart.CFrame.LookVector.X, rootPart.CFrame.LookVector.Y, rootPart.CFrame.LookVector.Z)
		RunService.RenderStepped:Wait()
	end

	-- Restore walk speed after dash
	updateWalkSpeed()

	wait(dashCooldownTime)
	canDash = true
end

-- Dash input handler (press Q)
UserInputService.InputBegan:Connect(function(input, processed)
	if processed then return end

	if input.KeyCode == Enum.KeyCode.Q then
		dash()
	end
end)

