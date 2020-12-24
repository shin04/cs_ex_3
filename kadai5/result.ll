@n = common global i32 0, align 4
@sum = common global i32 0, align 4
define i32 @main(){
  store i32 10, i32* @n, align 4
  store i32 0, i32* @sum, align 4
  br label 1
  1:
  %1 = load i32, i32* @n, align 4
  %2 = icmp sgt i32 0, %1
  br i1 %2, label 2, label 3
  2:
  %3 = load i32, i32* @sum, align 4
  %4 = load i32, i32* @n, align 4
  %5 = add nsw i32 %3, %4
  store i32 %5, i32* @sum, align 4
  %6 = load i32, i32* @n, align 4
  %7 = sub nsw i32 %6, 1
  store i32 %7, i32* @n, align 4
  br label 3
  3:
  ret i32 0
}
