@x = common i32 0, align 4
@y = common i32 0, align 4
@z = common i32 0, align 4
define i32 @main(){
  store i32 12, i32* @x, align 4
  store i32 20, i32* @y, align 4
  %1 = load i32, i32* @x, align 4
  %2 = load i32, i32* @y, align 4
  %3 = mul nsw i32 %1 %2
  store i32 %3, i32* @z, align 4
  ret i32 0
}
