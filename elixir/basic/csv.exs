defmodule CsvReader do
    defp splitCollums(lines) do
        [collums | values] = lines



        for idx, collum in enumerate(collums) do
            csv[collum] = Enum.reduce(values, fn value_row -> value_row[idx] end)
        end

        csv
    end

    # returns {collum: [values]}
    def readCsv(file_path) do
        File.read!(file_path)
        |> String.split("\n")
        |> splitCollums
    end
end

IO.inspect CsvReader.readCsv("my_csv.csv")
