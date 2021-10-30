local modpath = minetest.get_modpath(minetest.get_current_modname())
local mod_api_stom = io.open(modpath .. "/mod_api_stom", "w")
local mod_api_mtos = io.open(modpath .. "/mod_api_mtos", "r")
if not mod_api_stom or not mod_api_mtos then
	error("mod api isn't running")
end

local function api_write(r)
	mod_api_stom:write(minetest.write_json(r))
	mod_api_stom:write("\n")
	mod_api_stom:flush()
end

local function call_function(fid, ...)
	api_write({_function=fid, args={...}})
end

local get_results
local function create_wrapper_function(fid)
	return function(...)
		call_function(fid, ...)
		return unpack(get_results())
	end
end

local function pack_args(args)
	if type(args) == "table" then
		if args._function ~= nil then
			return create_wrapper_function(args._function)
		end

		for k, v in pairs(args) do
			args[k] = pack_args(v)
		end
	end

	return args
end

get_results = function()
	while true do
		local r = minetest.parse_json(mod_api_mtos:read("*l"))
		if type(r) == "table" and r._lua_function ~= nil then
			local args = pack_args(r.args)
			local ret = _G[r._lua_module][r._lua_function](unpack(args))
			api_write(ret)
		else
			return r
		end
	end
end

assert(get_results() == true)
