class Project < ApplicationRecord
  has_many :schedulers, dependent: :destroy

  has_many :resources,
           foreign_key: :reference_id,
           class_name: :ResourceProject,
           dependent: :destroy
end
