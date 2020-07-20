(python run_test.py "test_segment.sql" "test_segment_expected") || exit 1 
(python run_test.py "test_node.sql" "test_node_expected") || exit 1 
(python run_test.py "test_radius.sql" "test_radius_expected") || exit 1 