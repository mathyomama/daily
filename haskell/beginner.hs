import Data.Char

--First task is to print "Hello, World!"
main = putStrLn "Hello, World!"

--Second task is to return an array of the first 100 numbers divisible by 3 and 5 (i.e. divisible by 15?)
myList = [x | x <- [15,16..], x `mod` 3 == 0, x `mod` 5 == 0]

--Third task is to create a program which will verify if one word is an anagram of another
--I will create an if statement for this (didn't use it, oh well)
if' :: Bool -> a -> a -> a
if' True x _ = x
if' False _ y = y

noCaseCompare :: Char -> Char -> Bool
noCaseCompare a b = (toLower a) == (toLower b)

countCharInString :: String -> Char -> Int
countCharInString string character = length (filter (noCaseCompare character) string)

charAmountArray :: String -> String -> [Int]
charAmountArray string1 string2 = map (countCharInString string2) string1

anagram :: String -> String -> Bool
anagram string1 string2
	| l1 /= l2 = False
	| array1 == array2 = True
	| otherwise = False
	where (l1, l2, array1, array2) = (length string1, length string2, charAmountArray string1 string1, charAmountArray string1 string2)

--Fourth task is to remove a given character from a string (I am interpretting it as all matching characters)

removeChar :: String -> Char -> String
removeChar string char = filter (/=char) string

--Fifth task is to sum the components of an array

sum' :: (Num a) => [a] -> a
sum' [] = 0
sum' s@(x:xs) = x + (sum' xs)
