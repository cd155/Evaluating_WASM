export function fib(n: i32): i32 {
  var a = 0
  if (n === 0) return 0
  if (n === 1) return 1

  a = fib(n-1) + fib(n-2)
  return a
}