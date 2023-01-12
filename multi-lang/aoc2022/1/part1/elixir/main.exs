defmodule HighestFinder do
    defp make_integer(str) do
        try do
            String.to_integer(str)
        rescue
            _ -> 0
        end
    end

    def findHighest() do
        # this has to be defined here, kinda lame
        to_int = &make_integer/1
        add = &+/2

        File.read!("input")
        |> String.split("\n\n")
        |> Enum.map(&String.split(&1, "\n"))
        |> Enum.map(&Enum.map(&1, to_int))
        |> Enum.map(&Enum.reduce(&1, 0, add))
        |> Enum.max
    end
end

IO.puts HighestFinder.findHighest
