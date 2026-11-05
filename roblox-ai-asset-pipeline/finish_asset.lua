-- Step 4: finish the uploaded model in Roblox Studio.
-- Paste into Studio's command bar in Edit mode (or run through the Studio MCP server).

local InsertService = game:GetService("InsertService")

local ASSET_ID = 0 -- paste the asset ID from upload.py
local GROUND_Y = 0 -- top of the default Baseplate; change if your floor is elsewhere

-- One entry per Blender object name
local STYLES = {
	TreasureChest_Wood = { Color = Color3.fromRGB(122, 82, 48), Material = Enum.Material.WoodPlanks },
	TreasureChest_Metal = { Color = Color3.fromRGB(230, 170, 45), Material = Enum.Material.SmoothPlastic },
	TreasureChest_Gem = { Color = Color3.fromRGB(80, 200, 255), Material = Enum.Material.Neon, Light = true },
}

local model = InsertService:LoadAsset(ASSET_ID)
model.Name = "TreasureChest"
model.Parent = workspace

for _, part in model:GetDescendants() do
	if part:IsA("MeshPart") then
		part.Anchored = true
		local style = STYLES[part.Name]
		if style then
			part.Color = style.Color
			part.Material = style.Material
			if style.Light then
				part.CanCollide = false
				part.CastShadow = false
				local light = Instance.new("PointLight")
				light.Color = style.Color
				light.Range = 12
				light.Parent = part
			end
		else
			warn("No style for part: " .. part.Name)
		end
	end
end

-- Move the model so its bottom sits exactly on the ground
local boxCFrame, boxSize = model:GetBoundingBox()
local bottom = boxCFrame.Position.Y - boxSize.Y / 2
model:PivotTo(model:GetPivot() + Vector3.new(0, GROUND_Y - bottom, 0))

print("Finished", model.Name, "size:", boxSize)
