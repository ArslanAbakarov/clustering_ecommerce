function AddToCartClick(sender) {
	// alert("Added")
	sender.outerHTML = '<div class="added-item-button">In cart</div>';
	return 0;
}