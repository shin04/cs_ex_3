@n = common global i32 0, align 4
@sum = common global i32 0, align 4
define i32 @main(){
  store i32 10, i32* @n, align 4
  store i32 0, i32* @sum, align 4
  br label %1
  1:
  %2 = load i32, i32* @n, align 4
  %3 = icmp sgt i32 0, %2
  br i1 %3, label %4, label %10
  4:
  %5 = load i32, i32* @sum, align 4
  %6 = load i32, i32* @n, align 4
  %7 = add nsw i32 %5, %6
  store i32 %7, i32* @sum, align 4
  %8 = load i32, i32* @n, align 4
  %9 = sub nsw i32 %8, 1
  store i32 %9, i32* @n, align 4
  br label %10
  10:
  ret i32 0
}
