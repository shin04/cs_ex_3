@sum = common global i32 0, align 4
@i = common global i32 0, align 4
define i32 @main(){
  store i32 0, i32* @sum, align 4
  store i32 1, i32* @i, align 4
  br label %1
  1:
  %2 = load i32, i32* @i, align 4
  %3 = icmp slt i32 %2, 11
  br i1 %3, label %4, label %11
  4:
  %5 = load i32, i32* @sum, align 4
  %6 = load i32, i32* @i, align 4
  %7 = add nsw i32 %5, %6
  store i32 %7, i32* @sum, align 4
  br label %8
  8:
  %9 = load i32, i32* @i, align 4
  %10 = add nsw i32 %9, 1
  store i32 %10, i32* @i, align 4
  br label %1
  11:
  ret i32 0
}
