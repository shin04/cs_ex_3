@a = common global i32 0, align 4
define void @proc(){
  store i32 10, i32* @a, align 4
  ret void
}
define i32 @main(){
  call void @proc()
  ret i32 0
}
