extends Control
var click_count = 0
@export var main_counter : Label

func _ready() -> void:
	main_counter.text = "Score: " + str(click_count)

func _on_main_button_pressed() -> void:
	click_count += 1
	main_counter.text = "Score: " + str(click_count)
