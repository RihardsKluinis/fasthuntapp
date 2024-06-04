class ProjectsController < ApplicationController
    def index
      @projects = ProjectLaunch.all
    end
  end