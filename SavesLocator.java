import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Properties;
import java.util.stream.Stream;

/**
 * This program searches for all (Minecraft) save files in the selected Paths.
 */
public class SavesLocator {

    /**
     * Main Method of the Program
     * @param args Command Line Arguments
     */
    public static void main(String[] args) {
        Properties properties = new Properties();
        try {
            properties.load(new FileInputStream("config.properties"));

            // Create String Array for Paths
            String[] paths;

            // Check if Auto Search is enabled
            if (properties.getProperty("autoSearch").equals("true")) {
                // Search for Drives
                paths = File.listRoots().toString().split(" ");
            } else {
                // Get Paths from Properties
                paths = properties.getProperty("drives").split(",");
            }

            // Search for Saves
            String[] saves = searchSaves(paths);

            // Create File with saves
            createFile(paths, saves, properties.getProperty("outputFile"));

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * Searches for all Minecraft Save Files in the selected Paths
     * @param paths The paths to search
     */
    public static String[] searchSaves(String[] paths) {
        // Create String Array for Saves
        String[] saves = new String[0];

        // Search for Saves
        if (paths != null && paths.length > 0) {
            for (String path : paths) {

                /*
                Path searchPath = Paths.get(path);
                try(Stream<Path> pathStream = Files.find(searchPath, Integer.MAX_VALUE, (p, bfa) -> p.getFileName().toString().equals("level.dat"))) {
                    saves = pathStream.map(Path::toString).toArray(String[]::new);
                } catch (IOException e) {
                    e.printStackTrace();
                }
                */

                /*
                Path searchPath = Paths.get(path);
                try(java.util.stream.Stream<Path> files = java.nio.file.Files.walk(searchPath)) {
                    saves = files.filter(java.nio.file.Files::isDirectory)
                            .filter(p -> p.getFileName().toString().equals("level.dat"))
                            .map(Path::toString)
                            .toArray(String[]::new);
                } catch (IOException e) {
                    e.printStackTrace();
                }*/
            }
        }

        // Return Saves
        return saves;
    }

    // Create file with Paths to Save Files
    public static void createFile(String[] paths, String[] saves, String outputFile) {
        // Create String for Output
        StringBuilder output = new StringBuilder();
        output.append("Paths searched:\n");

        // Add Paths to Output
        if (paths != null && paths.length > 0) {
            for (String path : paths) {
                output.append(path).append("\n");
            }
        }
        output.append("Saves found:\n");

        // Add Saves to Output
        if (saves != null && saves.length > 0) {
            for (String save : saves) {
                output.append(save).append("\n");
            }
        }

        // Write Output to File
        try {
            File file = new File(outputFile);
            file.createNewFile();
            java.io.FileWriter writer = new java.io.FileWriter(file);
            writer.write(output.toString());
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
