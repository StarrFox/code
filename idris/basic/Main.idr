module Main

import Data.List
import Data.String

data Expr = Add | Subtract | Multiply | Divide

parseOperator : String -> Maybe Expr
parseOperator "+" = Just Add
parseOperator "-" = Just Subtract
parseOperator "*" = Just Multiply
parseOperator "/" = Just Divide
parseOperator _ = Nothing

calculate : Expr -> List Double -> Double
calculate Add nums = sum nums
calculate Subtract nums = foldr (-) (2 * head nums) nums
calculate Multiply nums = product nums
calculate Divide nums = foldr (/) (head nums * head nums) nums

eval : String -> Maybe Double
eval input = case words input of
  (opStr :: numStrs) => do
    op <- parseOperator opStr
    nums <- traverse parseDouble numStrs
    pure $ calculate op nums
  _ => Nothing

main : IO ()
main = do
  putStrLn "Enter your expression:"
  input <- getLine
  case eval input of
    Just result => putStrLn $ "Result: " ++ show result
    Nothing => putStrLn "Invalid expression."

