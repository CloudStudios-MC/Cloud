import os

def translate(line):
    translations = {
        "spawnZombie": "world.spawnEntity(location, EntityType.ZOMBIE);",
        "spawnSkeleton": "world.spawnEntity(location, EntityType.SKELETON);",
        
        "sendMessage": 'player.sendMessage("{message}");',
        
        "giveItem": 'player.getInventory().addItem(new ItemStack(Material.{item}));',
        
        "setBlock": 'world.getBlockAt({x}, {y}, {z}).setType(Material.{material});',
        
        "teleport": 'player.teleport(new Location(world, {x}, {y}, {z}));',
        
        "setTime": 'world.setTime({time});',
        
        "setWeather": 'world.setWeatherDuration({duration}); world.setWeatherType(WeatherType.{weather});',
        
        "giveExperience": 'player.giveExp({amount});',
        
        "runCommand": 'Bukkit.getServer().dispatchCommand(Bukkit.getServer().getConsoleSender(), "{command}");'
    }

    # Translate Cloud Commands to Java
    if line.startswith("spawnZombie()"):
        return translations["spawnZombie"]
    elif line.startswith("spawnSkeleton()"):
        return translations["spawnSkeleton"]
    elif line.startswith("sendMessage("):
        message = line.split('"')[1]
        return translations["sendMessage"].replace("{message}", message)
    elif line.startswith("giveItem("):
        parts = line.strip("giveItem(").strip(")").split(", ")
        item = parts[1].strip('"')
        return translations["giveItem"].replace("{item}", item.upper())
    elif line.startswith("setBlock("):
        parts = line.strip("setBlock(").strip(")").split(", ")
        x, y, z, material = parts[0], parts[1], parts[2], parts[3].strip('"')
        return translations["setBlock"].format(x=x, y=y, z=z, material=material.upper())
    elif line.startswith("teleport("):
        parts = line.strip("teleport(").strip(")").split(", ")
        x, y, z = parts[0], parts[1], parts[2]
        return translations["teleport"].format(x=x, y=y, z=z)
    elif line.startswith("setTime("):
        time = line.strip("setTime(").strip(")")
        return translations["setTime"].format(time=time)
    elif line.startswith("setWeather("):
        parts = line.strip("setWeather(").strip(")").split(", ")
        duration, weather = parts[0], parts[1].strip('"')
        return translations["setWeather"].format(duration=duration, weather=weather.upper())
    elif line.startswith("giveExperience("):
        amount = line.strip("giveExperience(").strip(")")
        return translations["giveExperience"].format(amount=amount)
    elif line.startswith("runCommand("):
        command = line.strip("runCommand(").strip(")").strip('"')
        return translations["runCommand"].format(command=command)
    else:
        return "// Unknown command"

# Example Cloud code
cloud_code = [
    'spawnZombie()',
    'setBlock(0, 64, 0, "stone")',
    'giveItem(player, "diamond_sword")',
    'sendMessage(player, "Welcome to the server!")',
    'teleport(player, 100, 64, 200)',
    'setTime(1000)',
    'setWeather(1200, "rain")',
    'giveExperience(player, 100)',
    'runCommand("say Hello World")'
]

# Compile the Cloud code to Java
def compile_cloud_file(cloud_code):
    # Java file header and imports
    translated_code = ["// Translated Cloud to Java\n\n"]
    translated_code.append("package com.example.plugin;\n\n")
    translated_code.append("import org.bukkit.Bukkit;\n")
    translated_code.append("import org.bukkit.Material;\n")
    translated_code.append("import org.bukkit.entity.Player;\n")
    translated_code.append("import org.bukkit.event.Listener;\n")
    translated_code.append("import org.bukkit.event.EventHandler;\n")
    translated_code.append("import org.bukkit.event.player.PlayerInteractEvent;\n")
    translated_code.append("import org.bukkit.plugin.java.JavaPlugin;\n")
    translated_code.append("import org.bukkit.World;\n")
    translated_code.append("import org.bukkit.Location;\n\n")

    # Plugin class declaration
    translated_code.append("public class GeneratedPlugin extends JavaPlugin implements Listener {\n\n")

    # onEnable method
    translated_code.append("    @Override\n")
    translated_code.append("    public void onEnable() {\n")
    translated_code.append("        getLogger().info(\"GeneratedPlugin has been enabled!\");\n")
    translated_code.append("        getServer().getPluginManager().registerEvents(this, this);\n")
    translated_code.append("    }\n\n")

    # onDisable method
    translated_code.append("    @Override\n")
    translated_code.append("    public void onDisable() {\n")
    translated_code.append("        getLogger().info(\"GeneratedPlugin has been disabled.\");\n")
    translated_code.append("    }\n\n")

    # Event handler
    translated_code.append("    @EventHandler\n")
    translated_code.append("    public void onPlayerInteract(PlayerInteractEvent event) {\n")
    translated_code.append("        Player player = event.getPlayer();\n")
    translated_code.append("        // Add your event handling logic here\n")
    translated_code.append("    }\n\n")

    # onCommand method
    translated_code.append("    public void onCommand(Player player, World world, Location location) {\n")

    # Translate each cloud command to Java and add it to the plugin
    for line in cloud_code:
        java_line = translate(line.strip())
        translated_code.append(f"        {java_line}\n")

    # Closing braces
    translated_code.append("    }\n")
    translated_code.append("}\n")

    # Write the Java code to a file
    java_file_path = os.path.join("java_output", "GeneratedPlugin.java")
    with open(java_file_path, 'w') as f:
        f.writelines(translated_code)

compile_cloud_file(cloud_code)

