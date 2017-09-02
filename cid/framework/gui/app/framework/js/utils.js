
// ------------------- UNIQUE ID -------------------

function max_id_in_collection(input_collection)
{
	let input_lists = input_collection.find('.input-list');
	
	return input_lists.get().map(input_list =>
	{
		return max_id_in_list($(input_list));
	}).reduce((a,b) => Math.max(a,b));
}

function max_id_in_list(input_list)
{
	let input_fields = input_list.find('.input-field');
	
	return input_fields.get().map(input_field =>
	{
		return parseInt($(input_field).attr('data-input-id').match(/\d+$/));
	}).reduce((a,b) => Math.max(a,b));
}

function get_new_id(new_input_li)
{
	let old_id = new_input_li.find('.input-field').attr('data-input-id');
	
	let input_collection = new_input_li.parents('.input-collection');
	if(input_collection.length)
	{
		var max_id = max_id_in_collection(input_collection);
	}
	else
	{
		var max_id = max_id_in_list(new_input_li.parents('.input-list'));
	}
	
	return old_id.replace(/\d+$/, max_id+1);
}
