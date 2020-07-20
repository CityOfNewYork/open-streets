-- lion
CREATE INDEX lionnodeidfrom ON lion (nodeidfrom);
CREATE INDEX lionnodeidto ON lion (nodeidto);
CREATE INDEX lionsegmentid  ON lion (segmentid);
alter table lion add column cartodb_id serial;
